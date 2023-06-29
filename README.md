# `isaac.3me.tudelft.nl`

> A high-powered shared computer operated by the Biomechanical Engineering Department at TU Delft

# Hardware Details

**tl;dr**: 2x64-core processors (256 threads), 256 GB memory, 2x RTX A5000 GPUs, 2 TB SSD, 8 TB HDD

| Interface | MAC Address | Physical Location |
| - | - | - |
| `enxb03af2b6059f` | `b0:3a:f2:b6:05:9f` | top port |
| `eno1np0` | `3c:ec:ef:ca:9b:70` | middle port (this is what is plugged into the TUD network) |
| `eno2np1` | `3c:ec:ef:ca:9b:71` | bottom port |

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

# OS Details

**tl;dr**: Ubuntu 22, Logical Volume Management (LVM)

| Server Detail | Value | Comment |
| - | - | - |
| Short name | isaac | Used in any documentation etc. |
| `hostname` | isaac | Machines network-exposed name |
| Internet Domain Name | `isaac.3me.tudelft.nl` | Globally true |
| Firewall | SSH (TCP/22) only (+ICMP) | All connections must be tunneled via SSH |

## SSH Details

```bash
$ ssh-keyscan -t ecdsa isaac.3me.tudelft.nl > key.pub
$ ssh-keygen -l -f key.pub -E md5
256 MD5:13:da:5f:04:d8:1d:f3:25:a6:5b:50:66:67:56:38:58 isaac.3me.tudelft.nl (ECDSA)
$ ssh-keygen -l -f key.pub -E sha256
256 SHA256:mc5iQGpMA7KzS4gxa1VrYj5aKLvq7qBwOS+DnkxxzM0 isaac.3me.tudelft.nl (ECDSA)
```
| SSH ECDSA | isaac.3me.tudelft.nl ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBEYIsORj6P8jGCvJFbQngiesjF0DGvtZunslHiRkTICdCsQQDLqsPORY/FcFNRyB04so1Mf1hVE5ZmlHYILnXzQ=


# Computer Details (Work in Progress)

- hostname: `isaac`
- SSH ECDSA: `SHA256:mc5iQGpMA7KzS4gxa1VrYj5aKLvq7qBwOS+DnkxxzM0`
- SSH ED25519 fingerprint: `SHA256:wYV24VyXQHTrLsTY01iD5jDZiy2mdJmhwn95HkQ1hM0`
- MAC addresses:

- Current local IP (temporary): `10.211.34.72`
- `uname -a`: `Linux isaac 5.15.0-60-generic #66-Ubuntu SMP Fri Jan 20 14:29:49 UTC 2023 x86_64 x86_64 x86_64 GNU/Linux`
- `nvidia-smi`: `NVIDIA-SMI 525.78.01    Driver Version: 525.78.01    CUDA Version: 12.0`
- Desktop stack: `xfce` X environment launched via TigerVNC

# Current Work Plan

- **Phase 1**: Setup core OS + drivers + SSH:

    - [x] Install Ubuntu as a base OS, because it’s typically the most popular Linux distro for end-users

    - [x] Ensure BIOS is configured to auto-boot into that OS

    - [x] Set up internet connection and SSH
    
        - [x] Plug in to wall
        - [x] Ensure TUD DHCP assigns the network interfaces an IP (i.e. there's a physical + ethernet + DHCP connection)
        - [x] Ticket IT to enable network access from the machine (requires MAC addr) - `C230113189`
        - [x] Handle ticket responses, etc. - fully resolve it
    
    - [x] Set up additional drivers (specificlly, Nvidia, CUDA, etc.)
    
    - [x] Create `sudo` accounts:
    
        - [x] `adam` - for initial setup
    
    - [x] Set up VNC such that users with SSH access an access a remote desktop for the machine.

    - [x] Set up a firewall such that the machine only accepts SSH connections (VNC would be *via* an SSH tunnel)
    
        - This is so that we know for a fact that the only way to access the machine is via a valid, encrypted, SSH tunnel with an active user account on the machine – it means we don’t have to security review all servers etc. that are running on the machine and we can activate/deactivate people by just deactivating their Linux account (rather than also having to deactivate accounts on other services hosted from the machine)
    
    - [ ] Ensure we can all connect to the machine and are happy with the basic connection + desktop setup
    - [x] Record network interface information (notably: MAC addresses) for IT ticketing later
    - [x] Ticket IT to reconfigure their network such that the machine operates as a server:

        - [x] Provide them with a MAC address
        - [x] Also request the domain name `isaac.3me.tudelft.nl`

    - [x] Ensure the machine can be connected to remotely via the address, etc.
    - [x] List any relevant driver/OS versions in this README

- **Phase 2**: Research commissioning:
 
    - [x] Setup GitHub repo for documenting, posting issues related to, etc. the machine (e.g. as we have for the CBL one: https://github.com/ComputationalBiomechanicsLab/systems)
    
    - [ ] Build and install any research-level software (OpenSim, FEBio, etc.).
        - [x] Firefox
        - [x] OpenSim Creator
        - [x] Python3
        - [x] MATLAB
        - [x] Anaconda (installed to `/opt/anaconda`, add to `/etc/profile`)
        - [x] Julia
        - [ ] OpenSim Core (no GUI - annoying to build on Linux)
        - [x] OpenSim Creator
        - [x] Blender
        - [ ] SCONE
        - [ ] FEBio? Abaqus? Tensorflow?
        - [ ] Try to document version numbers for the GitHub guide
    
    - [ ] Write user guide, similar to how we already do it for the CBL machine
    
    - [ ] Onboard researchers

 
- **Phase 3**: Maintenance
 
    - Mostly leave the machine alone until someone actually has a problem
    - Use the GitHub repo to document problems/changes
    - Occasionally (every couple of months) login and ensure there’s enough disk space, deactivate unused user accounts, generally just ensure the machine’s mostly fine
    - 

# Notes

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
