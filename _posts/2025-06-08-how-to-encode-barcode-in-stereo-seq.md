---
title: 'How to encode barcode in stereo-seq'
lang: en
license: true
aside:
  toc: true
show_edit_on_github: true
pageview: true
tags:
  - Stereo-seq
  - barcode
---
<img src="https://visitor-badge.laobi.icu/badge?page_id=https://labonom.github.io/2025/06/08/how-to-encode-barcode-in-stereo-seq.html" alt="visitor badge"/> [![GitHub](https://img.shields.io/badge/GitHub-Profile-black?logo=github)](https://github.com/LabOnoM)

I had made a silly story in this week.


🟢 **`mamba` is a drop-in replacement for `conda`**, but drastically faster for solving.

```bash 
conda install mamba -n base -c conda-forge
mamba create -n barcodeenv boost=1.73 hdf5=1.10.7 zlib=1.2.11 -c conda-forge
conda activate barcodeenv
mamba install -c conda-forge gcc_linux-64 gxx_linux-64
mamba install -c conda-forge boost=1.73
```


```bash
DIR_INC := ./inc
DIR_SRC := ./src
DIR_OBJ := ./obj

PREFIX ?= /usr/local
BINDIR ?= $(PREFIX)/bin

# Use Conda’s Boost, but system GCC
INCLUDE_DIRS = -I$(DIR_INC) -I$(CONDA_PREFIX)/include -I/usr/include/hdf5/serial
LIBRARY_DIRS = -L$(CONDA_PREFIX)/lib -L/usr/lib/x86_64-linux-gnu/hdf5/serial

SRC := $(wildcard ${DIR_SRC}/*.cpp)
OBJ := $(patsubst %.cpp,${DIR_OBJ}/%.o,$(notdir ${SRC}))

TARGET := ST_BarcodeMap-0.0.1
BIN_TARGET := ${TARGET}

CXX := g++
CXXFLAGS := -std=c++11 -g -O3 $(INCLUDE_DIRS)
LD_FLAGS := $(LIBRARY_DIRS) -lboost_serialization -lhdf5 -lz -lpthread

${BIN_TARGET}: ${OBJ}
	$(CXX) $(OBJ) -o $@ $(LD_FLAGS)

${DIR_OBJ}/%.o: ${DIR_SRC}/%.cpp make_obj_dir
	$(CXX) -c $< -o $@ $(CXXFLAGS)

.PHONY: clean
clean:
	rm -f ${DIR_OBJ}/*.o
	rm -f ${TARGET}

make_obj_dir:
	@if [ ! -d ${DIR_OBJ} ]; then mkdir -p ${DIR_OBJ}; fi

install:
	install ${TARGET} ${BINDIR}/${TARGET}
	@echo "Installed."
```

```bash
export LD_LIBRARY_PATH=$CONDA_PREFIX/lib:$LD_LIBRARY_PATH
./ST_BarcodeMap-0.0.1 --in A02598A4.barcodeToPos.h5 --out barcodes.txt --action 3
```


## References
- [https://github.com/STOmics/ST_BarcodeMap/issues/2](https://github.com/STOmics/ST_BarcodeMap/issues/2)
- [https://github.com/STOmics/ST_BarcodeMap](https://github.com/STOmics/ST_BarcodeMap)