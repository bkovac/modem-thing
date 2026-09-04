# Modem thing
## Converting a $20 4G wireless hotspot into a texting device

Read more in the blog post: [https://bkovac.github.io/modem-thing/](https://bkovac.github.io/modem-thing/)

But in short, this is a project which combines a MSM8916 based cheap chinese 4G hotpsot, a Clicks Keyboard and a Sharp memory display into a portable texting device.

This repo is used to store 3D models, board files, kernel patches, guides and scripts.

## Structure
```
├── docs                        # blog post hosted on GitHub Pages
├── enclosure                   # enclosure .step files
├── helper-pcb                  # helper PCB board files
├── scripts                     # some rando python scripts i used to debug the display
├── patches                     # my driver patches, one to build it, other for dithering
└── README.md                   # this README
```

## Compiling the driver

Get the kernel and stuff:
```
wget https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-6.12.1.tar.xz
tar xf linux-6.12.1.tar.xz 
cd linux-6.12.1/
cp ../from-the-dongle/live.config .config
export ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu-
make olddefconfig
make modules_prepare
```

Clone the original driver from [ardangelo/sharp-drm-driver](https://github.com/ardangelo/sharp-drm-driver) (all credit to the author btw) and apply my patches.

Then compile the thing:
```
<cd into the driver directory>
make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- LINUX_DIR=../linux-6.12.1/ KBUILD_MODPOST_WARN=1
```
