# POSITIVO M10 4G PRO X (T2040)

Árvore de dispositivo do TWRP para o Positivo M10 4G PRO X (Unisoc SC9863A, Android 10, 32 bits).

## Build (twrp-11)

```bash
repo init --depth=1 -u https://github.com/minimal-manifest-twrp/platform_manifest_twrp_aosp.git -b twrp-11
repo sync -c -j$(nproc) --force-sync --no-clone-bundle --no-tags
git clone <este repositório> device/positivo/t2040

export ALLOW_MISSING_DEPENDENCIES=true
. build/envsetup.sh
lunch twrp_t2040-eng
mka recoveryimage
```

A imagem sai em `out/target/product/t2040/recovery.img`.

## Observações

- `prebuilt/dtb` e `prebuilt/dtbo.img` devem vir do `recovery.img` original da mesma versão de firmware instalada no tablet, assim como `prebuilt/kernel`.
- O kernel só descompacta ramdisk em gzip.
- O fastboot do bootloader não grava o TWRP; grave pelo fastbootd do recovery original.
