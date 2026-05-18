

# updating packages
echo "[Task]: [ Updating all installed packages ]"
pip list --outdated | awk 'NR>2 {print $1}' | xargs -n1 pip install -U
echo "[Task]: [ Done ]"

# removing requirement file
echo "[Task]: [ Removing the existing requirement file ]"
rm -f requirements.txt
echo "[Task]: [ Done ]"

# creating and listing the packages
echo "[Task]: [ Creating file and listing the packages ]" 
pip freeze > requirements.txt
echo "[Task]: [ Done ]"