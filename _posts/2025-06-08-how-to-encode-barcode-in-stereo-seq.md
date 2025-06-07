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

I made a silly story this week...

<!--more-->

## Background
I wanted to extract only the reads located *within* the tissue to reduce the FASTQ file size for running [CARLIN](https://gitlab.com/hormozlab/carlin) analysis. These days, I rely heavily on AI. And this time, AI seriously misled me and wasted a lot of my time. Here's what happened.

## AI-explanations 
The `A02598A4.barcodeToPos.h5` file does not contain actual ATGC sequences, and I couldn’t find any documentation online about how to convert CID numbers into actual DNA barcodes. So, I turned to AI for help. AI responded:
  > **Your integer CIDs** are a compact representation of the CID DNA barcode. To use them for read filtering, you must **convert the integer to the DNA sequence** (typically 25 bases for Stereo-seq Bin50/100).
  > ## **How the Encoding Works**
  > - The integer is a **base-4 encoding** of the 25bp DNA CID barcode.  
  > - A=0, C=1, G=2, T=3 (least significant base is at the end).  
  > - You can convert any integer CID to its corresponding DNA sequence using a small script.
  
It's pretty great, right? The AI also kindly provides me a python script for converting the CID numbers into the actual sequence:
```Python
def cid_to_seq(cid_int):
    base4 = []
    for _ in range(25):
        base = cid_int % 4
        base4.append("ACGT"[base])
        cid_int //= 4
    return ''.join(reversed(base4))

print("25-mer:", cid_to_seq(cid_value))
```

In addition, AI backed its explanation with what seemed like credible references, as shown below:

<img src="https://github.com/LabOnoM/LabOnoM.github.io/blob/458492bcb707287bc9a10767ca27b4b84daca13c/_posts/PostAttachedFiles/AI_Response_20250604.png" />

I was convinced by the AI’s explanation after briefly skimming the online resources it cited, including:
 - [https://db.cngb.org/stomics/assets/html/stereo.seq.html](https://db.cngb.org/stomics/assets/html/stereo.seq.html)
 - [Chen A, Liao S, Cheng M, Ma K, Wu L, Lai Y, Qiu X, Yang J, Xu J, Hao S, Wang X. Spatiotemporal transcriptomic atlas of mouse organogenesis using DNA nanoball-patterned arrays. Cell. 2022 May 12;185(10):1777-92.](https://www.cell.com/cell/fulltext/S0092-8674(22)00399-3?dgcid=raven_jbs_etoc_email)
## Verify AI's CID2ATGC convert algorithm.
Let's use the example below

```
Read name = E150018299L1C036R00400117279  
Read length = 100bp  
Flags = 0  
----------------------  
Mapping = Primary @ MAPQ 255  
Reference span = chr3:129,504,132-129,504,231 (+) = 100bp  
Cigar = 100M  
Clipping = None  
----------------------  
XF = 4  
NH = 1  
HI = 1  
nM = 0  
UR = 6B507  
AS = 98  
Cx = 6518  
Cy = 12274

---

Location = chr3:129,504,138  
Base = A @ QV 34
```


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