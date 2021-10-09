
FROM ubuntu:18.04
RUN date
RUN apt-get update -y && apt install -y git libglib2.0-dev libgcrypt20-dev zlib1g-dev autoconf automake libtool bison flex libpixman-1-dev git

RUN git clone git://github.com/Xilinx/qemu.git && cd qemu && git checkout tags/xilinx-v2020.1 && git submodule update --init dtc 

COPY . qemu

RUN cd qemu && mkdir build && cd build && ../configure --enable-fdt --disable-kvm --disable-xen --enable-gcrypt && make -j4

