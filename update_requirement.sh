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

# New function added to check for package removals
function checking_for_removed_packages(){
    echo "[Task]: [ Start ]"
    echo "[Task]: [ Checking if any packages were removed during the upgrade ]"
    
    # Compare the pre-upgrade snapshot against the current post-upgrade state
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


function begin_prompt(){
    # prompting start of the script
    echo "[Task]: [ Begin ] ================== "
    echo ""
}

begin_prompt

echo "[Task]: [ Start ]"
echo "[Task]: [ Updating all installed packages ]"

# check first if there's outdated packages
outdated=$(pip list --outdated | awk 'NR>2 {print $1}')

if [ -n "$outdated" ]; then

    # Capture a snapshot of installed packages BEFORE the upgrade runs
    echo "[Task]: [ Capturing pre-upgrade snapshot of installed packages ]"
    pre_upgrade_snapshot=$(pip list | awk 'NR>2 {print $1}')

    # downloading newer packages
    echo "$outdated" | xargs -r pip install -U
    echo "[Task]: [ Done ]"
    echo " "

else
    # if everything is up to date
    echo "[Task]: [ Everything is already fully up to date. ]"
    echo "[Task]: [ Done ]"
    echo " "
fi

checking_for_removed_packages

removing_requirement_file

creating_requirement_file

# prompting the end of the script
echo "[Task]: [ Close ]  ================== "