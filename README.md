# `isaac.3me.tudelft.nl`

> A high-powered shared computer operated by the Biomechanical Engineering Department at TU Delft

## Table of Contents

- [Quickstart for existing users (Windows)](#quickstart)
- [Walkthrough for new users (Windows)](#walkthrough)
- [Hardware Details](#hardware-details)
- [OS Details](#os-details)
- [SSH Details](#ssh-details)
- [User Software Details](#user-software-details)
- [Other Notes](#other-notes)

## Quickstart for existing users (Windows) <a name="quickstart"></a>

This assumes you already went through the extensive walthrough below and
just want to reconnect:

- Open windows terminal
- Run `ssh -L 59000:localhost:<your vpn port> username@isaac.3me.tudelft.nl`
- Type in your password (**remember, you can't see it being typed in**)
- Open VNC viewer on your Windows machine
- Use your VNC password to connect
  - You can reset your VNC password from an SSH terminal with `bme_vnc-passwd`


## Walkthrough (Windows - you're a new user) <a name="walkthrough"></a>

This walkthrough essentially sets up:

- Using `ssh` to connect a terminal to `cbl1`
- Launching a personal VNC server on `cbl1`
- Opening an SSH tunnel to the VNC server
- Using VNC Viewer to connect to the tunneled VNC server

### 1. Connect to the server with SSH

> **Note**: this assumes you have been given SSH credentials by (e.g.) an
> admin. Your credentials will be a **username** + **password** combo. This combo
> differs from your general TU Delft credentials. Once you have logged into
> `cbl1.3me.tudelft.nl`, you can change your password in the terminal with `passwd`

All connections to `cbl1.3me.tudelft.nl` must go via an SSH tunnel. SSH is a
standard method for creating a secure connection to a remote machine. By "SSHing"
into a server, you gain access to a terminal that can be used to run things on
the server (via a command prompt).

You always need an SSH connection to connect to `cbl1` - even 
if you actually want a GUI (e.g. a remote desktop). Later steps in this guide
describe setting up a remote desktop *via* the SSH connection.

- Open a Windows PowerShell window

  - SHIFT + right-click on your Windows desktop

  - Click "Open PowerShell Window Here"

- SSH into the server with your login credentials by typing `ssh
  username@cbl1.3me.tudelft.nl`

- Enter your password. **Note: you can't see any changes while typing
  the password in (it's a security feature)**

- You should now have an SSH connection to `cbl1.3me.tudelft.nl`. It will print a
  welcome message, etc.

- If you only need  terminal access, you can stop reading this
  walkthrough - you're done :smile:


### 2. Boot a VNC server on `cbl1`

A VNC client is used to "remote desktop" connect to a VNC server on
`cbl1.3me.tudelft.nl`. Each user runs their own VNC server on `cbl1`.

- In your SSH session (established above) run `cbl_vnc-start`. If
  necessary, type a new VNC password. You can change the password
  later with `cbl_vnc-passwd`.

- The `cbl_vnc-start` command should, before completing, print some
  help documentation. From this, **you need to rememeber**:

  - The VNC password you set
    - **this is different from your SSH password**
    - It is limited to 6 characters
    - It does not need to be secure, because your VNC connection
      always goes via your (secure) SSH connection
  - The VNC server's port, printed in the terminal (e.g. `6901`)
    - The `cbl_vnc-start` should print this in a large banner, or some
      explanation text

- A VNC server is now running on `cbl1`. However, it is hidden behind
  `cbl1`'s firewall, which only permits SSH connections.


### 3. Setup a SSH tunnel to the VNC server

`cbl1` only allows external connections via SSH. All services
(e.g. VNC) must connect via an SSH tunnel. This step sets up a tunnel
through the SSH connection through to the VNC server you booted in the
previous step.

- Exit the SSH connection to `cbl1` that was used in previous steps by
  either:

  - Typing `exit` in the terminal (to `exit` the SSH session)
  - Pressing CTRL+D to interrupt+exit the terminal
  - Closing the Powershell window

- Open a new SSH session to `cbl1` with tunelling enabled by running
  the command below (note: `<your VNC server port>` is printed during
  the previous step):

```bash
ssh -L 59000:localhost:<your VNC server port> username@cbl1.3me.tudelft.nl

# example: ssh -L 59000:localhost:6901 adam@cbl1.3me.tudelft.nl
```

- You should now have a new SSH session open that looks exactly like
  the previous one. It is essentially the same, but now *also* tunnels
  any connections to `localhost:59000` on your machine to `<your VNC
  server port>` on `cbl1`.


### 4. Install + setup VNC client on your machine

- Download a VNC client. I used VNC Viewer, from [here](https://www.realvnc.com/en/connect/download/viewer/)

- Other VNC clients (e.g. Remmina) also seem to work, but I only
  tested with VNC Viewer on Windows


### 5. Use the client to connect to the VNC server via the tunnel

- In your VNC client, connect to `localhost:59000`, which is the
  local-side of your (opened in the previous step) SSH tunnel to your
  VNC server (also a previous step) on `cbl1`

- If you receive warnings about connection security (e.g. encyption)
  you can ignore these. The connection between the VNC client and
  `localhost:59000` is insecure, but local (to your machine). The
  actual data is transported via the (encrypted) SSH tunnel, which is
  secure - the VNC client doesn't "know" that's whats happening.

- Use your VNC password when connecting to the machine with the VNC
  client.

  - Note: you can change your password in the SSH session with
    `cbl_vnc-passwd`

  - Note #2: VNC passwords are usually max. 6 chars, so your usual
    password might've been truncated

- Once connected, you should see a (somewhat rough-looking) Linux
  desktop
  
You're done! woohoo! :smile:


## Hardware Details <a name="hardware-details"></a>

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

## OS Details <a name="os-details"></a>

**tl;dr**: Ubuntu 22, installed with Logical Volume Management (LVM)

| Server Detail | Value | Comment |
| - | - | - |
| Short name | isaac | Used in any documentation etc. |
| `hostname` | isaac | Machines network-exposed name |
| Internet Domain Name | `isaac.3me.tudelft.nl` | Globally true |
| Firewall | SSH (TCP/22) only (+ICMP) | All connections must be tunneled via SSH |

## SSH Details <a name="ssh-details"></a>

```bash
$ ssh-keyscan -t ecdsa isaac.3me.tudelft.nl > key.pub
$ ssh-keygen -l -f key.pub -E md5
256 MD5:13:da:5f:04:d8:1d:f3:25:a6:5b:50:66:67:56:38:58 isaac.3me.tudelft.nl (ECDSA)
$ ssh-keygen -l -f key.pub -E sha256
256 SHA256:mc5iQGpMA7KzS4gxa1VrYj5aKLvq7qBwOS+DnkxxzM0 isaac.3me.tudelft.nl (ECDSA)
```
| SSH ECDSA | isaac.3me.tudelft.nl ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBEYIsORj6P8jGCvJFbQngiesjF0DGvtZunslHiRkTICdCsQQDLqsPORY/FcFNRyB04so1Mf1hVE5ZmlHYILnXzQ=

## User Software Details <a name="user-software-details"></a>

| Software Package | Installation Method | Notes |
| - | - | - |
| Firefox | apt | Primary Web Browser |
| OpenSim Creator | manual source build + install | To validate @adamkewley's purpose in life |
| Python3 | apt | `Python 3.10` |
| MATLAB | manual binary install | R2022b |
| Anaconda | manual binary install | Installed to `/opt/anaconda`, added to `etc/profile`, so that all users can use `conda` etc in their terminals |
| Julia | apt | 1.8.5 |
| `opensim-core` | manual source build + install | Built + installed with script in this repo, has Moco and python support |
| Blender | manual binary install | 3.4.1 |
| SCONE | manual binary install | TODO |
| FEBio | manual binary install | TODO |
| Abaqus | manual binary install | TODO |
| Tensorflow | TODO | TODO |

# Other Notes <a name="other-notes"></a>

- LVM commands begin with prefixing `pv` for physical drive (volume), `vg` for volume group, and `lv` for logical volume within that group
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
