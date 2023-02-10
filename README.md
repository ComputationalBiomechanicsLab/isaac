# Computer Details (Work in Progress)

- hostname: `isaac`
- SSH ECDSA: `SHA256:mc5iQGpMA7KzS4gxa1VrYj5aKLvq7qBwOS+DnkxxzM0`
- SSH ED25519 fingerprint: `SHA256:wYV24VyXQHTrLsTY01iD5jDZiy2mdJmhwn95HkQ1hM0`
- MAC addresses:

| interface | `link/ether` | phyiscal location |
| - | - | - |
| `enxb03af2b6059f` | `b0:3a:f2:b6:05:9f` | top port |
| `eno1np0` | `3c:ec:ef:ca:9b:70` | middle port |
| `eno2np1` | `3c:ec:ef:ca:9b:71` | bottom port |

- Current local IP (temporary): `10.211.34.72`

# Current Work Plan

- **Phase 1**: Setup core OS + drivers + SSH:

    - [x] Install Ubuntu as a base OS, because it’s typically the most popular Linux distro for end-users

    - [x] Ensure BIOS is configured to auto-boot into that OS

    - [x] Set up internet connection and SSH
    
        - [x] Plug in to wall
        - [x] Ensure TUD DHCP assigns the network interfaces an IP (i.e. there's a physical + ethernet + DHCP connection)
        - [x] Ticket IT to enable network access from the machine (requires MAC addr) - `C230113189`
        - [x] Handle ticket responses, etc. - fully resolve it
    
    - [ ] Set up additional drivers (specificlly, Nvidia, CUDA, etc.)
    
    - [ ] Create `sudo` accounts:
    
        - [x] `adam` - for initial setup
        - [ ] ~~`ajay`, `mathias`~~ - establish which users definitely need sudo access, because it's dangerous
    
    - [ ] Set up VPN such that users with SSH access an access a remote desktop for the machine.

    - [ ] Set up a firewall such that the machine only accepts SSH connections (VPN would be *via* an SSH tunnel)
    
        - This is so that we know for a fact that the only way to access the machine is via a valid, encrypted, SSH tunnel with an active user account on the machine – it means we don’t have to security review all servers etc. that are running on the machine and we can activate/deactivate people by just deactivating their Linux account (rather than also having to deactivate accounts on other services hosted from the machine)
    
    - [ ] Ensure we can all connect to the machine and are happy with the basic connection + desktop setup
    - [ ] Record network interface information (notably: MAC addresses) for IT ticketing later
    - [ ] Ticket IT to reconfigure their network such that the machine operates as a server:

        - [ ] Provide them with a MAC address
        - [ ] Also request the domain name `isaac.3me.tudelft.nl`

    - [ ] Ensure the machine can be connected to remotely via the address, etc.

- **Phase 2**: Research commissioning:
 
    - [ ] Setup GitHub repo for documenting, posting issues related to, etc. the machine (e.g. as we have for the CBL one: https://github.com/ComputationalBiomechanicsLab/systems)
    
    - [ ] Build and install any research-level software (OpenSim, FEBio, etc.).
        - [ ] OpenSim Core (no GUI - annoying to build on Linux)
        - [ ] OpenSim Creator
        - [ ] SCONE
        - [ ] FEBio? Abaqus? Blender? Tensorflow?
        - [ ] Try to document version numbers for the GitHub guide
    
    - [ ] Write user guide, similar to how we already do it for the CBL machine
    
    - [ ] Onboard researchers

 
- **Phase 3**: Maintenance
 
    - Mostly leave the machine alone until someone actually has a problem
    - Use the GitHub repo to document problems/changes
    - Occasionally (every couple of months) login and ensure there’s enough disk space, deactivate unused user accounts, generally just ensure the machine’s mostly fine
