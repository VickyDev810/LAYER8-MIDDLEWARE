## ENCLAVE SIMULATION
```markdown
# 🛡️ Run Python Anonymizer Inside Gramine Enclave

This guide helps you run a simple Python script or FastAPI app inside a [Gramine](https://gramineproject.io/) enclave, using simulation or SGX hardware.

---

## 🧰 Prerequisites

- Docker installed
- Intel SGX drivers (if running with SGX)

---

## 📦 Step 1: Download & Run Gramine Docker Image

Pull the Gramine Docker image (or build your own if needed):

```bash
docker pull gramineproject/gramine:latest
```

Run the Gramine environment inside Docker:

```bash


docker run -it --rm \
  -v /absolute/path/to/enclave_simulation:/gramine-app \
  --security-opt seccomp=unconfined \
  my-gramine-env \
  bash
```

**Replace `/absolute/path/to/enclave_simulation` with your actual project path.**

## 📁 Step 2: Navigate to the Mounted App Folder

Inside the Docker container, run:

```bash
cd /gramine-app
```

This is your working directory inside the container.

## 🛠️ Step 3: Build the Manifest

Use `make` to compile the manifest and prepare the Gramine environment.

**For simulation mode (no SGX hardware):**

```bash
make
```

**For real SGX hardware:**

```bash
make SGX=1
```

This generates the file:

```
python.manifest
```

This is generated from `python.manifest.template` or `python.manifest.example`.

## ▶️ Step 4: Run the App in Enclave

Run your Python script with Gramine:

**Without SGX (simulation mode):**

```bash
gramine python scripts/anonymize_sample.py
```

**With Intel SGX:**

```bash
gramine-sgx python scripts/anonymize_sample.py
```

**Without SGX:**

```bash
gramine-direct python scripts/anonymize_sample.py
```



