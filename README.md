# Ansible Systems Toolkit

[![commitizen friendly](https://img.shields.io/badge/commitizen-friendly-brightgreen.svg)](http://commitizen.github.io/cz-cli/)
[![license](https://img.shields.io/npm/l/@rfgamaral/parcel-plugin-typings-for-css-modules.svg)](LICENSE)

This repository contains a set of [Ansible](https://www.ansible.com/) playbooks and roles needed to set up and configure all of my systems, which I've automated to document all configuration changes in case I ever need to start from scratch or apply a similar configuration to another system. Although they are somewhat specific to my systems, I've decided to publish them because they may be useful to someone else.

**Warning:** If you want to give these playbooks and roles a try, you should first fork this repository, carefully review the code, and remove things you don’t want or need. Don’t blindly use my playbooks unless you know what that entails.

## Playbooks

### POLYMERBOX

This playbook configures my Raspberry Pi, which handles my home network core services (e.g., [AdGuard Home](https://github.com/AdguardTeam/AdGuardHome) DNS server).

#### How to provision from zero?

1. Burn the Raspberry Pi OS Lite (32-bit) image to an SD card with [Raspberry Pi Imager](https://github.com/raspberrypi/rpi-imager/releases);
2. Before putting the SD card on the Raspberry Pi, mount it on your computer and:
    - Enable the SSH server by creating an empty `ssh` file in the **boot** partition.
    - (Optional) Disable Wi-Fi by adding `dtoverlay=disable-wifi` to the `config.txt` in the **boot** partition.
3. Unmount the SD card, put it on the Raspberry Pi, and boot it;
4. Wait a couple of minutes for the Raspberry Pi to cycle-boot at least once;
5. Open your favorite terminal and run the following command to perform the initial configuration:

    ```
    ansible-playbook ./playbooks/polymerbox.yml --tags bootstrap
    ```

    Essentially what this does is, updates your local machine know SSH public keys for the new remote host, creates a specific administrator account and deletes the default `pi` account (check the [`playbook.yml`](playbooks/polymerbox.yml) file for more details).

    **Note:** This command is meant to be executed **once** after burning a new image to an SD card. The playbook will fail at the `debian/accounts/create-admin-user` task if you attempt to run it a second time.

6. While on the terminal run the following command to perform the main configuration:

    ```
    ansible-playbook ./playbooks/polymerbox.yml
    ```

    This will configure the base system settings and services, upgrade the distribution software and kernel, set up the administrator and root accounts dotfiles, and install and configure additional software (check the [`playbook.yml`](playbooks/polymerbox.yml) file for more details).

#### How to upgrade the distribution software and kernel?

Some tasks in the playbook are tagged so that one can easily use Ansible to keep the system up to date with the latest software releases, patches, and fixes. To perform a full upgrade just run the following command on your terminal:

```
ansible-playbook ./playbooks/polymerbox.yml --tags upgrade
```

## User Guide

### Encrypted Variables

If you've looked through all the files in this repository, you may have noticed that some configuration variables are encrypted since they contain sensitive data that should not be shared.

If you want to use these playbooks for yourself, you have two options:

1. If you have no intention of sharing your modified playbooks with anyone else you might as well ignore the encrypted variables altogether. In other words, just change the variables to literal strings instead of encrypted strings.

2. If you have the intention of sharing your modified playbooks with the world just as I did, here's the setup I'm currently using for this repository:
    - Generate a long and random password for the vault and store it your password manager for safekeeping;
    - Create a `.password` (unversioned) file in the root of the repository and put the generated password there;
    - Use the `ansible-vault encrypt_string` command to create an encrypted variable (check the [documentation](https://docs.ansible.com/ansible/latest/user_guide/vault.html#use-encrypt-string-to-create-encrypted-variables-to-embed-in-yaml) for more details);
    - Ansible is configured to automatically pick the vault password from the root `.password` file for any playbook (check the [`ansible.cfg`](ansible.cfg) file for more details).

If you're not comfortable with any of the options above, please look into the [Ansible Vault](https://docs.ansible.com/ansible/latest/user_guide/vault.html) user guide for other ways on how to keep your sensitive data secure.

### Inventory Hosts

As you can see from looking at the [`inventory.cfg`](inventory.cfg) file, I use a fully qualified domain name (FQDN) for all my hosts. These are known as _host alias_ in Ansible and it's what Ansible will use to connect to the hosts.

If you want to use these playbooks for yourself, there are two important things you should know:

- Regardless of the host alias you pick (FQDN or not), your network needs to resolve that name to an IP address so that Ansible can connect to the host. There are so many ways one could do this - I have an internal DNS server doing it for me - but the easiest way is to point the `ansible_host` variable to the host IP address in your inventory file (check the [documentation](https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html#inventory-aliases) for more details).

- Some roles were written to read host-specific files and variables based on the **exact** host alias specified in the inventory file. If you look at the [playbooks](playbooks/) directory, you'll see that files are stored in the `playbooks/files/<host-alias>/` folder and variables are defined in the `playbooks/host_vars/<host-alias>.yml` file. Please keep this in mind when editing playbooks to fit your needs.

### Shorter Commands

This repository is configured as an [npm](https://www.npmjs.com) package with the sole purpose of having shorter commands to perform all the configuration steps detailed below for each one of the playbooks.

If you are an npm user, just install the necessary dependencies with `npm install` (or `yarn install`) and look at the [`package.json`](package.json) file to learn about the alias commands you can use with `npm run <command>` (or `yarn run <command>`) instead of the full commands.

## License

The use of this source code is governed by an MIT-style license that can be found in the [LICENSE](LICENSE) file.
