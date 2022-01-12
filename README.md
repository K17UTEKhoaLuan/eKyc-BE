# eKyc-BE

## How to run code?

### 1. Setup machine

#### Install Python 3

##### - Window

Install by [link](https://www.python.org/downloads/)

##### - Ubuntu

```bash
sudo apt install python3 python3-pip
```

#### Install Cmake

##### - Window

Install by [link](https://cmake.org/download/)

##### - Ubuntu

```bash
sudo apt install cmake
```

### 2. Clone code

```bash
git clone https://github.com/K17UTEKhoaLuan/eKyc-BE.git && cd eKyc-BE
```

### 3. Create logs

In folder `eKyc-BE` create folder __`logs`__ and create file `logs/log.log`

### 4. Install Packages

```bash
pip3 install -r requirements.txt
```

### 5. Run server

```bash
uvicorn app:app --port=5000 --host=0.0.0.0
```
