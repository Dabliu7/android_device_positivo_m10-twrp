#!/usr/bin/env python3
"""Gera um vbmeta para Unisoc que aceita o recovery assinado com a chave de teste do AOSP.

Lê o vbmeta original do aparelho, mantém as chaves de todas as partições
encadeadas e troca apenas a chave das partições indicadas em --resign
(por padrão, recovery). O resultado é assinado com a mesma chave de teste
e recebe o rodapé DHTB que o bootloader da Unisoc espera.

Rode a partir da raiz do código-fonte do TWRP:

    python3 device/positivo/t2040/tools/make_vbmeta.py \\
        --stock vbmeta-sign.img --out vbmeta-twrp.img
"""
import argparse
import hashlib
import os
import struct
import subprocess
import sys
import tempfile

VBMETA_PADDED_SIZE = 16384
IMAGE_SIZE = 1024 * 1024
DHTB_OFFSET = IMAGE_SIZE - 512
CHAIN_TAG = 4


def read_chains(data):
    """Devolve [(partição, rollback_index_location, chave_pública)] do vbmeta."""
    if data[:4] != b'AVB0':
        sys.exit('erro: o arquivo original não é um vbmeta (falta o cabeçalho AVB0)')
    auth_size, _aux_size = struct.unpack('>QQ', data[12:28])
    desc_offset, desc_size = struct.unpack('>QQ', data[96:112])
    pos = 256 + auth_size + desc_offset
    end = pos + desc_size
    chains = []
    while pos < end:
        tag, length = struct.unpack('>QQ', data[pos:pos + 16])
        body = data[pos + 16:pos + 16 + length]
        if tag == CHAIN_TAG:
            location, name_len, key_len = struct.unpack('>III', body[:12])
            name = body[76:76 + name_len].decode()
            key = body[76 + name_len:76 + name_len + key_len]
            chains.append((name, location, key))
        pos += 16 + length
    return chains


def dhtb_footer(vbmeta):
    footer = bytearray(512)
    footer[0:4] = b'DHTB'
    footer[4:8] = struct.pack('<I', 1)
    footer[8:40] = hashlib.sha256(vbmeta).digest()
    footer[48:52] = struct.pack('<I', len(vbmeta))
    return bytes(footer)


def wrap_image(vbmeta):
    if len(vbmeta) != VBMETA_PADDED_SIZE:
        sys.exit('erro: vbmeta gerado com %d bytes, esperado %d' % (len(vbmeta), VBMETA_PADDED_SIZE))
    image = bytearray(IMAGE_SIZE)
    image[:len(vbmeta)] = vbmeta
    image[DHTB_OFFSET:] = dhtb_footer(vbmeta)
    return bytes(image)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--stock', required=True, help='vbmeta original do aparelho (vbmeta-sign.img)')
    parser.add_argument('--out', required=True, help='arquivo de saída')
    parser.add_argument('--avbtool', default='external/avb/avbtool')
    parser.add_argument('--key', default='external/avb/test/data/testkey_rsa4096.pem')
    parser.add_argument('--resign', default='recovery',
                        help='partições que passam a usar a chave de teste, separadas por vírgula')
    args = parser.parse_args()

    for path in (args.stock, args.avbtool, args.key):
        if not os.path.isfile(path):
            sys.exit('erro: arquivo não encontrado: %s' % path)

    with open(args.stock, 'rb') as f:
        chains = read_chains(f.read())
    if not chains:
        sys.exit('erro: o vbmeta original não tem partições encadeadas')

    resign = [p for p in args.resign.split(',') if p]
    missing = [p for p in resign if p not in [c[0] for c in chains]]
    if missing:
        sys.exit('erro: partição ausente no vbmeta original: %s' % ', '.join(missing))

    with tempfile.TemporaryDirectory() as tmp:
        test_pub = os.path.join(tmp, 'testkey.bin')
        subprocess.check_call([sys.executable, args.avbtool, 'extract_public_key',
                               '--key', args.key, '--output', test_pub])
        cmd = [sys.executable, args.avbtool, 'make_vbmeta_image',
               '--key', args.key, '--algorithm', 'SHA256_RSA4096', '--flags', '0',
               '--padding_size', str(VBMETA_PADDED_SIZE)]
        for name, location, key in chains:
            key_path = test_pub
            if name not in resign:
                key_path = os.path.join(tmp, name + '.bin')
                with open(key_path, 'wb') as f:
                    f.write(key)
            cmd += ['--chain_partition', '%s:%d:%s' % (name, location, key_path)]
            print('%-14s local %2d  chave %s' % (name, location, 'de teste' if name in resign else 'original'))
        raw = os.path.join(tmp, 'vbmeta.img')
        subprocess.check_call(cmd + ['--output', raw])
        with open(raw, 'rb') as f:
            vbmeta = f.read()

    with open(args.out, 'wb') as f:
        f.write(wrap_image(vbmeta))
    print('gerado: %s (%d bytes)' % (args.out, IMAGE_SIZE))


if __name__ == '__main__':
    main()
