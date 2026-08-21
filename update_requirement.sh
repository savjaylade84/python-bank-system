#!/usr/bin/env bash

function begin_prompt(){
    # prompting start of the script
    echo "[Task]: [ Begin ] ================== "
    echo ""
}

function removing_requirement_file(){
    # removing requirement file
    echo "[Task]: [ Start ]"
    echo "[Task]: [ Removing the existing requirement file ]"
    rm -f requirements.txt
    echo "[Task]: [ Done ]"
    echo " "
}

function creating_requirement_file(){
    # creating and listing the packages
    echo "[Task]: [ Start ]"
    echo "[Task]: [ Creating requirement file and listing the packages ]"
    pip freeze > requirements.txt
    echo "[Task]: [ Done ]"
    echo " "
}

# Checks for package removals by comparing pre/post upgrade snapshots
function checking_for_removed_packages(){
    echo "[Task]: [ Start ]"
    echo "[Task]: [ Checking if any packages were removed during the upgrade ]"

    local removed_packages
    removed_packages=$(comm -23 <(echo "$pre_upgrade_snapshot" | sort) <(pip list | awk 'NR>2 {print $1}' | sort))

    if [ -n "$removed_packages" ]; then
        echo "[Task]: [ ALERT: The following packages were removed or replaced: ]"
        echo "$removed_packages" | while read -r pkg; do
            echo "[Task]: [ Removed: $pkg ]"
        done
    else
        echo "[Task]: [ No packages were removed during the upgrade process ]"
    fi
    echo "[Task]: [ Done ]"
    echo " "
}

# Safely updates packages: allows minor/patch bumps, skips major-version jumps
function safe_update_packages(){
    echo "[Task]: [ Start ]"
    echo "[Task]: [ Updating packages safely (minor/patch only, skipping major bumps) ]"

    local skipped_packages=()
    local failed_packages=()

    # pip list --outdated columns: Package  Version  Latest  Type
    # NR>2 skips the header row and the "----" separator row
    while read -r pkg current_version new_version _; do
        [ -z "$pkg" ] && continue

        current_major=$(echo "$current_version" | cut -d. -f1)
        new_major=$(echo "$new_version" | cut -d. -f1)

        if [ "$current_major" == "$new_major" ]; then
            echo "[Task]: [ Updating $pkg: $current_version -> $new_version (same major, safe) ]"
            if ! pip install -U "$pkg" >/dev/null 2>&1; then
                echo "[Task]: [ WARNING: $pkg failed to update ]"
                failed_packages+=("$pkg")
            fi
        else
            echo "[Task]: [ SKIPPING $pkg: $current_version -> $new_version (major version jump, needs manual review) ]"
            skipped_packages+=("$pkg ($current_version -> $new_version)")
        fi
    done < <(pip list --outdated | awk 'NR>2 {print $1, $2, $3}')

    echo " "
    if [ ${#skipped_packages[@]} -gt 0 ]; then
        echo "[Task]: [ The following packages have MAJOR updates available but were skipped: ]"
        for item in "${skipped_packages[@]}"; do
            echo "[Task]: [ - $item ]"
        done
    fi

    if [ ${#failed_packages[@]} -gt 0 ]; then
        echo "[Task]: [ The following packages FAILED to update: ]"
        for item in "${failed_packages[@]}"; do
            echo "[Task]: [ - $item ]"
        done
    fi

    echo "[Task]: [ Done ]"
    echo " "
}

begin_prompt

echo "[Task]: [ Start ]"
echo "[Task]: [ Checking for outdated packages ]"

# Capture a snapshot of installed packages BEFORE checking for/running the upgrade
# (must happen unconditionally, so the later comparison is always valid)
echo "[Task]: [ Capturing pre-upgrade snapshot of installed packages ]"
pre_upgrade_snapshot=$(pip list | awk 'NR>2 {print $1}')

outdated=$(pip list --outdated | awk 'NR>2 {print $1}')

if [ -n "$outdated" ]; then
    safe_update_packages
else
    echo "[Task]: [ Everything is already fully up to date. ]"
    echo "[Task]: [ Done ]"
    echo " "
fi

checking_for_removed_packages

removing_requirement_file

creating_requirement_file

# prompting the end of the script
echo "[Task]: [ Close ]  ================== "