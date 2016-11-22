#!/bin/bash

set -o errexit
set -o nounset
set -o pipefail

vm_prefix="${1:-openshiftdevel_openshiftdevel}"

echo "[INFO] Gathering information..."
if ! VBoxManage list vms | grep -q "${vm_prefix}"; then
        echo "[FATAL] No VM with name prefix \`${vm_prefix}\` found!"
        exit 1
fi

if [[ "$( VBoxManage list vms | grep "${vm_prefix}" | wc -l )" -gt 1 ]]; then
        echo "[FATAL] More than one VM with name prefix \`${vm_prefix}\` found!"
        exit 1
fi

vm_uuid="$( VBoxManage list vms | grep "${vm_prefix}" | grep -Po "(?<=\{).*(?=\})" )"
echo "[INFO] Found VM \`${vm_uuid}\`."

vm_info="$( VBoxManage showvminfo "${vm_uuid}" --machinereadable )"
vm_storage_controller="$( grep -Po "(?<=storagecontrollername0=\").*(?=\")" <<<"${vm_info}"  )"
echo "[INFO] Found storage controller \`${vm_storage_controller}\`"

if [[ "$( grep -q "${vm_storage_controller}\-ImageUUID" <<<"${vm_info}" | wc -l )" -gt 1 ]]; then
        echo "[FATAL] Found too many disks for controller \`${vm_storage_controller}\`!"
        exit 1
fi

vm_hdd_uuid="$( grep -Po "(?<=\"${vm_storage_controller}\-ImageUUID\-[0-9]\-[0-9]\"=\").*(?=\")" <<<"${vm_info}" )"
vm_hdd_port="$( grep -Po "(?<=\"${vm_storage_controller}\-ImageUUID\-)[0-9](?=\-[0-9]\"=)" <<<"${vm_info}" )"
vm_hdd_device="$( grep -Po "(?<=\"${vm_storage_controller}\-ImageUUID\-[0-9]\-)[0-9](?=\"=)" <<<"${vm_info}" )"
echo "[INFO] Found HDD \`${vm_hdd_uuid}\` as device \`${vm_hdd_device}\` on port \`${vm_hdd_port}\`."

vm_hdd_capacity="$( VBoxManage showmediuminfo "${vm_hdd_uuid}" | grep -Po "(?<=Capacity:       )[0-9]+(?= MBytes)" )"
echo "[INFO] Determined HDD capacity to be \`${vm_hdd_capacity}\`MB."

echo "[INFO] Expanding HDD capacity by 20GB..."
VBoxManage clonemedium disk "${vm_hdd_uuid}" hdd_clone.vdi --format vdi
VBoxManage modifymedium disk hdd_clone.vdi --resize "$(( vm_hdd_capacity + 20480 ))"
VBoxManage clonemedium disk hdd_clone.vdi expanded_hdd.vmdk --format vmdk

echo "[INFO] Swapping HDDs for VM \`${vm_uuid}\`..."
VBoxManage storageattach "${vm_uuid}"                            \
                         --storagectl "${vm_storage_controller}" \
                         --port "${vm_hdd_port}"                 \
                         --device "${vm_hdd_device}"             \
                         --type hdd                              \
                         --medium none
VBoxManage storageattach "${vm_uuid}"                            \
                         --storagectl "${vm_storage_controller}" \
                         --port "${vm_hdd_port}"                 \
                         --device "${vm_hdd_device}"             \
                         --type hdd                              \
                         --medium expanded_hdd.vmdk

echo "[INFO] Cleaning up intermediates..."
VBoxManage closemedium disk "${vm_hdd_uuid}"
rm hdd_clone.vdi

echo "[SUCCESS] Finished expanding disk size for VM."