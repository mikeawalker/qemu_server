
FROM ubuntu:18.04
RUN date
# Get all the dependencies we need for qemu
RUN apt-get update -y && apt install -y git libglib2.0-dev libgcrypt20-dev zlib1g-dev autoconf automake libtool bison flex libpixman-1-dev git
# Git clone QEMU
RUN git clone git://github.com/Xilinx/qemu.git && cd qemu && git checkout tags/xilinx-v2020.1 && git submodule update --init dtc
# Build qemu
# target-list can be modified to support other processors
RUN cd qemu && mkdir build && cd build && ../configure --target-list="aarch64-softmmu,microblazeel-softmmu" --enable-fdt --disable-kvm --disable-xen --enable-gcrypt && make -j4 
#copy stuff out of QEMU binary folders into bin so they can be run
#RUN cp /qemu/build/microblazee1-softmmu/qemu-system-microblazeel /usr/local/bin
#RUN cp /qemu/build/aarch64-softmmu/qemu-system-aarch64 /usr/local/bin

# get python to run the guu
RUN apt-get install -y python3 python3-pip

# get the python dependencies for the gui
RUN mkdir /home/gui
RUN mkdir /home/qemu

COPY gui /home/gui

RUN cd /home/ && pip3 install -r gui/requirements.txt
# Expose the following ports for the GUI
EXPOSE 5000

# Setup a volume for user to locate binary files
VOLUME /home/work

# Run the python GUI