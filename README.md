# 🖥️ `isaac.3me.tudelft.nl`

> A high-powered shared computer operated by the Biomechanical Engineering Department at TU Delft

## 📖 Table of Contents

- [Quickstart for existing users (Windows)](#quickstart)
- [Walkthrough for new users (Windows)](#walkthrough)
  1. [Connect to the server with SSH](#walkthrough-step-1)
  2. [Boot a VNC server on `isaac`](#walkthrough-step-2)
  3. [Setup a SSH tunnel to the VNC server](#walkthrough-step-3)
  4. [Install + setup VNC client on your machine](#walkthrough-step-4)
  5. [Use the client to connect to the VNC server via the tunnel](#walkthrough-step-5)
- [Hardware Details](#hardware-details)
- [OS Details](#os-details)
- [SSH Details](#ssh-details)
- [FAQs](#faq)
  1. [Q: How do I create my own Conda Environment?](#faq-q-conda-env-setup)
  2. [Q: How do I setup tensorflow?](#faq-q-tensorflow-setup)
  3. [Q: How do I setup OpenSim Python Scripting?](#faq-q-opensim-python-setup)
  4. [Q: How do I run ABAQUS jobs?](#faq-q-abaqus-jobs)
  5. [Q: How do I copy files to/from Isaac?](#faq-q-copy-files)
- [User Software Details](#user-software-details)
  1. [Logical Volume Management (LVM) Commands](#other-lvm-commands)
  2. [How to install ABAQUS on Ubuntu](#other-how-to-install-abaqus)
- [Other Notes](#other-notes)

## ⚡ Quickstart for existing users (Windows) <a name="quickstart"></a>

This assumes you already went through the [walkthrough](#walkthrough) below and
just want to reconnect:

- Open a terminal
- Run `ssh -L 59000:localhost:<your vnc port> username@isaac.3me.tudelft.nl`
- Type in your password (**remember, you can't see it being typed in**)
- Open your VNC client (VNC Connect, TightVNC Viewer, etc.) on your Windows machine
- Use your VNC password to connect

> ℹ️ **Note**
>
> - If you don't remember your user password, you'll have to ask an admin to reset it for you
> - If you don't remember your VNC port, you can restart your VNC server with `bme_vnc-restart`
> - If you don't remember your VNC password, you can reset it via your SSH session with `bme_vnc-passwd`


## 🚶 Walkthrough (Windows - you're a new user) <a name="walkthrough"></a>

This walkthrough sets up:

1. Using `ssh` to connect a terminal to `isaac`
2. Launching a personal VNC server on `isaac`
3. Opening an SSH tunnel to the VNC server
4. Setting up a VNC client on your computer
5. Using the VNC client to connect to your VNC server via the SSH tunnel

---
### 1. Connect to the server with SSH <a name="walkthrough-step-1"></a>

> ℹ️ **Note**: this assumes you already have SSH credentials
>
> - An isaac admin will give you a `username` + `password` combo. The combo differs from your TU Delft credentials
> - Once you have logged into `isaac.3me.tudelft.nl`, you can change your password in the terminal with `passwd`

All connections to `isaac.3me.tudelft.nl` must go via an SSH tunnel. SSH is a
standard method for creating a secure connection to a remote machine. By "SSHing"
into a server, you gain access to a remote terminal on `isaac` that you can use to
run things on it. You always need an SSH connection to connect to `isaac` - even
if you ultimately plan on using VNC to forward a remote GUI desktop. 

**To set up an SSH connection to `isaac.3me.tudelft.nl` on a Windows machine**:

- Open a Windows PowerShell window

  - SHIFT + right-click on your Windows desktop

  - Click "Open PowerShell Window Here"

- SSH into the server with your login credentials by typing `ssh
  YOUR_USERNAME@isaac.3me.tudelft.nl`

- Enter your password. **Note: you can't see anything being typed while typing
  your password in (it's a security feature)**

- You should now have an SSH connection to `isaac.3me.tudelft.nl`. It will print a
  welcome message, etc.

- If you only need  terminal access, you can stop reading this
  walkthrough - you're done :smile:

---
### 2. Boot a VNC server on `isaac` <a name="walkthrough-step-2"></a>

A VNC server is a piece of software that runs hosts a GUI desktop on
a machine (here, it'll be hosting a desktop *from* `isaac`). A VNC
client is a piece of software that connects to VNC servers and
presents the remote desktop to a user.

Each user on `isaac` hosts their own VNC server within their user account,
which means that you can reset it, keep it running overnight while your
laptop is turned off, change the password, etc.

**To set up a VNC server on `isaac`**:

- In your SSH session (established above) run `bme_vnc-start`. If
  necessary, type a new VNC password. You can change the password
  later with `bme_vnc-passwd`.

- The `bme_vnc-start` command should, before completing, print your
  VNC server's details. **You should note down**:

  - The VNC password you set
    - **this is different from your SSH password**
    - It is limited to 6 characters
    - It does not need to be secure, because your VNC connection
      always goes via your (secure) SSH connection
  - The VNC server's port, printed in the terminal (e.g. `6901`)
    - The `bme_vnc-start` should print this in a large banner, or some
      explanation text

After running `bme_vnc-start`, your VNC server should now be running on
running on `isaac`. Remember, though, that the only way to connect to it
is via an SSH tunnel (isaac's and TUD's firewalls only permit the SSH
connection), so we need to set up a tunnel.

---
### 3. Setup a SSH tunnel to the VNC server <a name="walkthrough-step-3"></a>

`isaac` only allows external connections via SSH. All services
(e.g. VNC) must connect via an SSH tunnel. This step sets up a tunnel
through the SSH connection through to the VNC server you booted in the
previous step.

**To setup an SSH tunnel for your VNC client on isaac**:

- (If your SSH session is still open in a terminal), exit your existing
  SSH connection to `isaac` by either:

  - Typing `exit` in the terminal (to `exit` the SSH session)
  - Pressing CTRL+D to interrupt+exit the terminal
  - Closing the Powershell window

- Open a new SSH session to `isaac` with tunelling enabled by running
  the command below (note: `<your VNC server port>` is printed during
  the previous step):

```bash
ssh -L 59000:localhost:<your VNC server port> YOUR_USERNAME@isaac.3me.tudelft.nl

# example: ssh -L 59000:localhost:6901 adam@isaac.3me.tudelft.nl
```

- Your terminal should now be connected via a new SSH session to `isaac`. It will
  look identical to your previous SSH session, but it now *also* tunnels that you
  make to `localhost:59000` on your machine to `<your VNC server port>` on `isaac`.

---
### 4. Install + setup VNC client on your machine <a name="walkthrough-step-4"></a>

To connect to the VNC server you booted on `isaac` in previous steps, you'll need a
VNC client. This walkthrough outlines using TightVNC which, while barebones-looking, is
functional and open-source.

> Note: Previous versions of this guide used VNC Connect. This guide is essentially the
> same as the previous versions, but was switched to TightVNC because of license concerns.

**To install a VNC client on your computer**:

- Download TightVNC from: https://www.tightvnc.com/download.php
- Install it
- Open it up, it should present a UI where you can enter a `Remote Host` etc.

---
### 5. Use the client to connect to the VNC server via the tunnel <a name="walkthrough-step-5"></a>

Once you have a VNC client, you need to boot it up and connect to `isaac` **via the ssh
tunnel**, so that you can then remotely control `isaac` via a remote desktop.

**To connect to your VNC server on `isaac` with the VNC client on your computer**:

- In your VNC client, connect to `localhost:59000`, which is the
  local-side of your (opened in the previous step) SSH tunnel to your
  VNC server (also a previous step) on `isaac`

- If you receive warnings about connection security (e.g. encryption)
  you can ignore these. The connection between the VNC client and
  `localhost:59000` is insecure, but local (to your machine). The
  actual data is transported via the (encrypted) SSH tunnel, which is
  secure - the VNC client doesn't "know" that's whats happening.

- Use your VNC password when connecting to the machine with the VNC
  client.

  - Note: you can change your password in the SSH session with
    `isaac_vnc-passwd`

  - Note #2: VNC passwords are usually max. 6 chars, so your usual
    password might've been truncated

- Once connected, you should see a (somewhat rough-looking) Linux
  desktop

---
### 6. Celebrate 🎉

![screenshot](images/vnc-desktop-screenshot.png)

If you see a remote desktop, you're done :smile:!


## 🤖 Hardware Details <a name="hardware-details"></a>

**tl;dr**: 2x64-core processors (256 threads), 256 GB memory, 2x RTX A5000 GPUs, 2 TB SSD, 8 TB HDD

| Interface | MAC Address | Physical Location |
| - | - | - |
| `enxb03af2b6059f` | `b0:3a:f2:b6:05:9f` | closest to PSU |
| `eno1np0` | `3c:ec:ef:ca:9b:70` | middle from PSU |
| `eno2np1` | `3c:ec:ef:ca:9b:71` | farthest from PSU |

```bash
# count physical processors
$ cat /proc/cpuinfo | grep 'physical id' | sort | uniq | wc -l
2
# print processor model name(s)
$ cat /proc/cpuinfo | grep 'model name' | sort | uniq
model name      : AMD EPYC 7713 64-Core Processor
# num threads
$ nproc
256
# total memory
$ cat /proc/meminfo | grep MemTotal
MemTotal:       263900564 kB
# show GPU information
$ nvidia-smi -L
GPU 0: NVIDIA RTX A5000 (UUID: GPU-56081830-3ba8-ab02-7439-1fa0f4452be5)
GPU 1: NVIDIA RTX A5000 (UUID: GPU-c9247f85-b247-45fa-edbc-1f794911a0b5)
# disk info (physical - note: LVM is being used here)
$ lsblk
sda                         8:0    1   7.3T  0 disk
sr0                        11:0    1  1024M  0 rom
nvme0n1                   259:0    0   1.8T  0 disk
├─nvme0n1p1               259:1    0     1G  0 part /boot/efi
├─nvme0n1p2               259:2    0     2G  0 part /boot
└─nvme0n1p3               259:3    0   1.8T  0 part
  └─ubuntu--vg-ubuntu--lv 253:0    0   100G  0 lvm  /var/snap/firefox/common/host-hunspell
```

## 🕹️ OS Details <a name="os-details"></a>

**tl;dr**: Ubuntu 22, installed with Logical Volume Management (LVM)

| Server Detail | Value | Comment |
| - | - | - |
| Short name | isaac | Used in any documentation etc. |
| `hostname` | isaac | Machines network-exposed name |
| Internet Domain Name | `isaac.3me.tudelft.nl` | Globally true |
| Firewall | SSH (TCP/22) only (+ICMP) | All connections must be tunneled via SSH |

## 🔒 SSH Details <a name="ssh-details"></a>

```bash
$ ssh-keyscan -t ecdsa isaac.3me.tudelft.nl > key.pub
$ ssh-keygen -l -f key.pub -E md5
256 MD5:13:da:5f:04:d8:1d:f3:25:a6:5b:50:66:67:56:38:58 isaac.3me.tudelft.nl (ECDSA)
$ ssh-keygen -l -f key.pub -E sha256
256 SHA256:mc5iQGpMA7KzS4gxa1VrYj5aKLvq7qBwOS+DnkxxzM0 isaac.3me.tudelft.nl (ECDSA)
```
| SSH ECDSA | isaac.3me.tudelft.nl ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBEYIsORj6P8jGCvJFbQngiesjF0DGvtZunslHiRkTICdCsQQDLqsPORY/FcFNRyB04so1Mf1hVE5ZmlHYILnXzQ=

## 💾 User Software Details <a name="user-software-details"></a>

| Software Package | Installation Method | Notes |
| - | - | - |
| Firefox | apt | Primary Web Browser |
| OpenSim Creator | manual source build + install | Validates @adamkewley's purpose in life |
| Python3 | apt | `Python 3.11.5` |
| MATLAB | manual binary install | R2022b |
| Anaconda | manual binary install | Installed to `/opt/anaconda`. Added to `PATH` via `etc/profile` |
| Julia | apt | 1.8.5 |
| `opensim-core` | manual source build + install | `4.4.1`, installed in `/usr/local`, see `setup_scripts/opensim.sh` for build details |
| Blender | manual binary install | `3.4.1`` |
| SCONE | manual binary install | `2.2` |
| FEBio | manual binary install | `2.3.0` |
| Abaqus | manual binary install | TODO |
| Tensorflow | pip install on base system and base conda env | `2.13.1` |
| `gfortran` / `gcc` / `g++` | apt | `11.4.0` |


## FAQs <a name="faq"></a>

### 1. Q: How do I create my own Conda Environment? <a name="faq-q-conda-env-setup"></a>

A: You can either:

- **If you're using a remote GUI desktop via VNC**:
  - Open `anaconda-navigator` via a terminal
  - Click `Environments` on the left-side in Anaconda Navigator
  - Create a new environment
  - Ensure your new environment is activated
  - All applications booted via the navigator should then use your new environment

- **If you're using a terminal (e.g. via SSH)**:
  - Ensure you have initialized `conda` for your terminal: `conda init` (reopen your shell with `exit` etc.)
  - List available python versions with `conda search python`
  - Create it via (e.g.) `conda create --name your_envname  python=3.8.18`
  - Activate it via `conda activate your_envname`
  - Test it with (e.g.) `python --version` (should print `Python 3.8.18` if following the other example commands)


### 2. Q: How do I setup tensorflow? <a name="faq-q-tensorflow-setup"></a>

A: `isaac` (the base system) has been configured with the appropriate NVIDIA,
Cuda, cuDNN, and TensorRT libraries, so you can run ad-hoc tensorflow tests
in that. E.g.:

```bash
/usr/bin/python3 -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
```

**The recommended way to run research software is to use conda, though**. This
is because your research code may use a different set of libraries in conjunction
with tensorflow. The `base` environment on `isaac` has one version installed:

```bash
conda run -n base python -c "import tensorflow as tf; print(tf.config.list_physical_devices(\'GPU\'))"
```

But, for your research, it is recommended that you create your own, new, `conda`
environment, install your version of `tensorflow` (+ your other libs) into it,
and then ensure it all works together. See "How do I create my own Conda Environment?"
above for a quick overview of how to do that.

Specifically, you'll end up writing something like below. Quick testing on `isaac`
indicates that you'll need to use python >= 3.10 for GPU acceleration to work:

```bash
# example setup
#
# the code below was tested with:
#
# - WORKS:  3.11.5  (conda create --name test_tensorflow python=3.11.5)
# - WORKS:  3.10.13 (conda create --name test_tensorflow python=3.10.13)
# - BROKEN: 3.9.18  (conda create --name test_tensorflow python=3.9.18)
# - BROKEN: 3.8.18  (conda create --name test_tensorflow python=3.8.18)

conda create --name test_tensorflow python=3.11.5
conda install -n test_tensorflow cudatoolkit cudnn tensorflow[and-cuda]
conda run -n test_tensorflow python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"

# if GPU acceleration is working, the `conda run` should print:
#     [PhysicalDevice(name='/physical_device:GPU:0', device_type='GPU'), PhysicalDevice(name='/physical_device:GPU:1', device_type='GPU')]
# (i.e. "tensorflow thinks isaac has two GPUs")

# activate the environment with `conda activate test_tensorflow`
```

### 3. Q: How do I setup OpenSim Python Scripting? <a name="faq-q-opensim-python-setup"></a>

A: The easiest way to use the OpenSim API via Python is to use a conda
environment as they outline [here](https://simtk-confluence.stanford.edu:8443/display/OpenSim/Conda+Package). The
conda forge page for the package, where you can find more information, is [here](https://anaconda.org/opensim-org/opensim).

These steps must be performed in a terminal (Anaconda Navigator was being extremely
iffy about it):

```bash
# BEFORE STARTING, SEE: https://anaconda.org/opensim-org/opensim/files to figure
# out which versions of python are supported by opensim

# add conda-forge channel
conda config --remove channels conda-forge

# create relevant conda environment that can use OpenSim
conda create --channel conda-forge --name my_env_name python=3.11.5

# activate the environment
conda activate my_env_name

# install opensim into the environment
conda install -c opensim-org opensim

# test that it works (should print OpenSim's version to the console)
python -c "import opensim; print(opensim.__version__);"
```

You can then use `my_env_name` (or whatever you called it) in the terminal, or
activate it via Anaconda Navigator (the problems I encountered were only during
installation).


### 4. Q: How do I run ABAQUS jobs? <a name="faq-q-abaqus-jobs"></a>

ABAQUS is available via a console using the `abq` command. This command links
to the installation folder, which you can find with `echo $(readlink -f $(which abq))`:

```bash
echo $(readlink -f $(which abq))
# at time of writing, prints: /opt/SIMULIA/EstProducts/2022/linux_a64/code/bin/SMALauncher
```

So, if `abq` isn't enough, other commands are available (at time of writing) in
`/opt/SIMULIA/EstProducts/2022/linux_a64/code/bin/`.

If you want to see the ABAQUS GUI, you'll need to access isaac via a VNC remote
desktop (described above), because SSH alone isn't enough to view GUIs. Once you
are on a VNC desktop, open a console and run `abq cae` to boot the UI.


### 5. Q: How do I copy files to/from Isaac? <a name="faq-q-copy-files"></a>

Your SSH connection also enables the ability to copy files to/from the machine
into any folder your user account is allowed to write to (usually, your home
folder, which includes your Desktop, and `/tmp`). All major OSes have an `scp`
command for doing this:

```bash
# e.g. open a PowerShell (Windows), GNOME (Linux), or Terminal (Mac) window in
# the directory you want to upload from, then:
scp -r file-or-folder-to-copy YOUR_USERNAME@isaac.3me.tudelft.nl:where-it-goes-on-server
```

This will copy `file-or-folder-to-copy` to the path that's specified after the
colon (`:`, in this case, `where-it-goes-on-server`).

Alternatively, if you find using a terminal a little daunting/tedious, there
are UI's available that do the same job (google: SSH copy files UI, SSHFS copy
files, etc.). A popular Windows client is [WinSCP](https://winscp.net/eng/index.php).

## 🗒️ Other Notes <a name="other-notes"></a>

### 1. Logical Volume Management (LVM) Commands <a name="other-lvm-commands"></a>

LVM commands begin with prefixing `pv` for physical drive (volume), `vg` for volume group, and `lv` for logical volume within that group

```bash
# the OS+homedirs are currently on a volume group for the SSD
$ sudo vgdisplay
  --- Volume group ---
  VG Name               ubuntu-vg
  System ID
  Format                lvm2
  Metadata Areas        1
  Metadata Sequence No  5
  VG Access             read/write
  VG Status             resizable
  MAX LV                0
  Cur LV                2
  Open LV               1
  Max PV                0
  Cur PV                1
  Act PV                1
  VG Size               <1.82 TiB
  PE Size               4.00 MiB
  Total PE              476150
  Alloc PE / Size       476134 / <1.82 TiB
  Free  PE / Size       16 / 64.00 MiB
  VG UUID               H6iHHH-op2X-thyQ-19NJ-aDDd-tDwl-hPFKpj

  --- Volume group ---
  VG Name               vg0
  System ID
  Format                lvm2
  Metadata Areas        1
  Metadata Sequence No  1
  VG Access             read/write
  VG Status             resizable
  MAX LV                0
  Cur LV                0
  Open LV               0
  Max PV                0
  Cur PV                1
  Act PV                1
  VG Size               <7.28 TiB
  PE Size               4.00 MiB
  Total PE              1907721
  Alloc PE / Size       0 / 0
  Free  PE / Size       1907721 / <7.28 TiB
  VG UUID               SayMzO-67ou-P0fK-XGOp-dQxz-ZlQb-F3wQdW

# And those groups are sliced up into "OS" and "homedirs":
$ sudo lvdisplay
  --- Logical volume ---
  LV Path                /dev/ubuntu-vg/ubuntu-lv
  LV Name                ubuntu-lv
  VG Name                ubuntu-vg
  LV UUID                rTjqnp-j9tz-nVLh-kKJC-9TpN-4qig-9N2Mb6
  LV Write Access        read/write
  LV Creation host, time ubuntu-server, 2023-01-23 14:07:13 +0000
  LV Status              available
  # open                 1
  LV Size                100.00 GiB
  Current LE             25600
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           253:0

  --- Logical volume ---
  LV Path                /dev/ubuntu-vg/homedirs
  LV Name                homedirs
  VG Name                ubuntu-vg
  LV UUID                HCdDUH-0PZ8-CFTX-uBDR-vwWe-FcvS-eV9zT3
  LV Write Access        read/write
  LV Creation host, time isaac, 2023-06-29 12:18:03 +0000
  LV Status              available
  # open                 0
  LV Size                <1.72 TiB
  Current LE             450534
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           253:1
```

### 2. How to install ABAQUS on Ubuntu <a name="other-how-to-install-abaqus"></a>

> ℹ️ **Note**
>
> This is effectively a condensed version of notes from the related [issue](https://github.com/ComputationalBiomechanicsLab/isaac/issues/12),
> where you might find more, but scattered, information.

ABAQUS doesn't officially support Ubuntu, so some hacks were necessary. Here
is a **rough** list of the steps taken on `isaac`:

- **SYSTEM CHANGE**: Switched Debian's `sh` implementation from `dash` (Debian's default) to `bash` (what
  ABAQUS actually requires). This was done system-wide by deleting the existing `sh --> dash`
  softlink in `/usr/bin` and replacing it with `sh --> bash` with `rm sh && ln -s bash sh`. It's
  necessary because ABAQUS's install scripts contain bash-specific syntax.

- **SYSTEM CHANGE**: Edited `/etc/hosts` `127.0.1.1 isaac` entry to `127.0.0.1 isaac`. The
  old entry is a legacy thing. Changing it is necessary if you want `abq verify all` to pass
  (see issue #12 for comments on why, but tl;dr, the verification suite uses ssh via the
  hostname and assumes it's == `localhost`).

- **APT DEPENDENCY INSTALL**: These were mentioned in [this](https://github.com/imirzov/Install-Abaqus-2019-on-Ubuntu-18.04-LTS) guide,
  but might not be necessary (I didn't check):

```bash
sudo apt install ksh gcc g++ gfortran libstdc++5 build-essential make libjpeg62
sudo apt install libmotif-dev libmotif-common rpm
```

- **DEPENDENCY INSTALL**: Installed Intel OneAPI via the method described [here](https://gist.github.com/SomajitDey/aeb6eb4c8083185e06800e1ece4be1bd).
  It's necessary because open-source FORTRAN compilers (e.g. `gfortran`) fail ABAQUS's `abq verify all` test suite. Here's
  a copy of the code that was ran on Isaac:

```bash
curl -Lo- https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB | sudo gpg --dearmor -o /usr/share/keyrings/oneapi-archive-keyring.gpg
sudo tee /etc/apt/sources.list.d/oneAPI.list <<< "deb [signed-by=/usr/share/keyrings/oneapi-archive-keyring.gpg] https://apt.repos.intel.com/oneapi all main"
sudo apt update
sudo apt install intel-oneapi-compiler-fortran
# sudo apt install intel-oneapi-mkl  # optional

# optionally, add this to `~/.bashrc` to source it:
# source /opt/intel/oneapi/setvars.sh > /dev/null
```

- **SYSTEM CHANGE**: Softlink the Intel OneAPI FORTRAN compiler system-wide as `ifort`, which is
  how ABAQUS addresses it (e.g. in scripts). This is necessary for `abq verify all` to pass.

```bash
ln -s /opt/intel/oneapi/compiler/latest/bin/ifort ifort
```

- **LOCAL ENVIRONMENT CHANGE**: Following [this](https://github.com/imirzov/Install-Abaqus-2019-on-Ubuntu-18.04-LTS)
  guide, it's necessary to set `DSYAuthOS` etc. to "fool" the ABAQUS installer scripts into accepting Ubuntu
  as the OS (otherwise, you'll get "OS not supported" messages):

```bash
# you need to set up your environment with this _before_ running `StartGUI.sh` installers etc.
export DSYAuthOS_`lsb_release -si`=1 DSY_Force_OS=linux_a64
```

- **GET ABAQUS INSTALLER+HOTFIX**: Received an ABAQUS and hotfix installer from a license
  holder (in my case, Mathias P). Directories received were called (e.g.) `golden` (presumably,
  for ABAQUS "gold" release) and `hotfix`. The `golden` directory expanded out to a bunch (~6)
  of `tar` files called (e.g.) `2022.AM_SIM_Abaqus_Extend.AllOS.1-5.tar`

- **UNPACK/COPY INSTALLER TO /opt/abq2022**: As described in [source](https://github.com/imirzov/Install-Abaqus-2019-on-Ubuntu-18.04-LTS) guide,
  copied the files to `/opt` and `chmod`ded them appropriately. Dir looked something like:

```bash
(base) adam@isaac:~/Desktop/abq2022/golden$ ls
 2022.AM_SIM_Abaqus_Extend.AllOS.1-5.tar   2022.AM_SIM_Abaqus_Extend.AllOS.3-5.tar   2022.AM_SIM_Abaqus_Extend.AllOS.5-5.tar   AM_SIM_Abaqus_Extend.AllOS                    PDir_SIMULIA_EstPrd
 2022.AM_SIM_Abaqus_Extend.AllOS.2-5.tar   2022.AM_SIM_Abaqus_Extend.AllOS.4-5.tar   Abaqus_2022.PDir_SIMULIA_EstPrd.1-1.tar  'Download Platform - Dassault Systèmes®.pdf'
```

- **BOOT VNC SERVER ON `root` ACCOUNT**: follow the SSH+VNC setup on the `root` account (not your own account with `sudo`). This
  is necessary because the GUI installer seemed like the most reliable, but it _must_ be ran as `root`. If you (e.g.) try
  running it on a non-`root` account (e.g. with `sudo`) then you'll end up with weird X-window-server issues where the
  installer can't open a `root`-level window for your non-`root` account.

- **INSTALL VIA `root` VNC**:

  - Login to remove VNC desktop as `root`
  - Open terminal
  - Ensure **LOCAL ENVIRONMENT** is setup in the terminal (described above): "export DSYAuthOS_`lsb_release -si`=1 DSY_Force_OS=linux_a64"
  - Run the `StartGUI.sh` installer (e.g. `/opt/abq2022/golden/AM_SIM_Abaqus_Extend.AllOS/1/StartGUI.sh`)
  - Install to default directory, but with `/usr/` switched for `/opt` (i.e. install it to `/opt`)
  - Follow the same procedure for `hotfix`

- **CONFIGURE LICENSE**:

  - Edit license file: `/opt/SIMULIA/EstProducts/2022/linux_a64/SMA/site/EstablishedProductsConfig.ini`
  - Add licensing information:

```ini
[EstablishedProducts]
LICENSE_SERVER_TYPE=flex
FLEX_LICENSE_CONFIG=27000@HIDDEN_ASK_MATHIAS_SHOULD_BE_DN
```

- **VERIFY**:

  - `abq` executable located at: `/opt/DassaultSystemes/SIMULIA/Commands/abq2022hf10` (depends on hotfix, or `hf`, level)
  - Verify by running it with `verify all`:

```bash
/opt/DassaultSystemes/SIMULIA/Commands/abq2022hf10 verify all
```

  - See [issue #12](https://github.com/ComputationalBiomechanicsLab/isaac/issues/12) for any issues I encountered
    when ensuring everything verifies

- **LINK AS `abq` SYSTEM-WIDE**: This is so that users just have to write `abq`, rather than
  needing to know the year, hotfix level, where it's installed, etc:

```bash
cd /usr/local/bin && ln -s /opt/DassaultSystemes/SIMULIA/Commands/abq2022hf10 abq
```
