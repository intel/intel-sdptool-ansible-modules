# Intel(R) SDP Tool Ansible Collection
Intel(R) SDP Tool Ansible plugin is an Ansible action plugin, which provides
Intel(R) Server Debug and Provisioning Tool (SDP Tool) capabilities in an
action plugin. The plugin enables all the functionalities of the SDP Tool.
The inventory file can feed in the required paths for the appropriate files.
A sample of the inventory file is available in the project which can be 
customized and used. A sample playbook is also provided to assist in writing
a customized playbook. Please find more information on the capabilities /
usage of the SDP Tool in the following link.
[Intel(R) Server Debug and Provisioning Tool](https://downloadcenter.intel.com/download/30410/Intel-Server-Debug-and-Provisioning-Tool-Intel-SDP-Tool-)

## Pre-requisites
- Ansible >= 2.10.x
- Python >=3.6.5
- `pexpect`\
  Python package
- Intel SDP Tool >= v2.0.0\
  Install Intel(R) SDP Tool from [here](https://downloadcenter.intel.com/download/30410/Intel-Server-Debug-and-Provisioning-Tool-Intel-SDP-Tool-) on the Ansible Controller

## Playbook
```yaml
---
# Sample Play
- name: Demo Playbook
  hosts: BMC
  gather_facts: True
  collections:
    - intel.sdptool  # Intel Collection required
  tasks:
    - name: CPU Information
      sdptool:
        action: "cpuinfo"       # action is mandatory check SDP Tool UserGuide for more commands
      register: output
    - name: SDPTool Output
      debug:
        msg: "{{ output.stdout_lines }}"
    - name: Save SEL logs
      sdptool:
        action: "sel"
        args:                   # args is optional, Refer SDP Tool UserGuide for more information
          - "-f"
          - "sellog.txt"
      register: output
    - name: SDPTool Output
      debug:
        msg: "{{ output.stdout_lines }}"
```

## Inventory
Host Variables:
- **bmc_username**: BMC username (Required, User can use other means to provide these details to the Ansible framework as well)
- **bmc_password**: BMC password (Required, User can use other means to provide these details to the Ansible framework as well)

The following variables are command specific and will be required variable :

- **ini_path**: syscfg file path for command - set_biosconfig_all
- **vmedia_iso_path**: iso path for vmedia
    - Samba share path with username and password
    - ISO or IMG file path
- **unmount_iso_path**: iso path for unmount
    - Samba share path with username and password
    - ISO or IMG file path
- **sup_path**: SUP directory path for update, command - update
- **custom_sup_path**: SUP directory path for custom_deploy,command - custom_deploy

```ini
# Sample Inventory
[BMC]
BMC_IP bmc_username=user bmc_password=password
```

## Running sanity, unit and integration tests
- Create standard directory structure
    ```bash
    mkdir -p ansible_collections/intel
    cd ansible_collections/intel
    ```
- Clone the repository from github and rename it to sdptool
    ```bash
    git clone https://github.com/intel/intel-sdptool-ansible-modules.git ./sdptool
    ```
- Setup python virtual environment
    ```bash
    virtualenv venv
    source venv/bin/activate
    ```
- Install devel ansible branch
    ```bash
    pip install https://github.com/ansible/ansible/archive/devel.tar.gz --disable-pip-version-check
    ```
- Run Sanity Test
    ```bash
    ansible-test sanity --docker default -v --color
    ```
- Run Unit Test
    ```bash
    ansible-test units --docker default -v --color
    ```
- Run Integration Test
    ```bash
    ansible-test integration -v --color
    ```

## Documentation
Run `ansible-doc` command to view plugin documentation.
```bash
ansible-doc intel.sdptool.sdptool
```
