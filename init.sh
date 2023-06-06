# To execute from the project directory
RED='\033[0;33m'
NC='\033[0m'

# Global path of the project to ~/.atmi
pwd > ~/.atmi

# Check the dependencies
echo -e "${RED}Checking the dependencies ...${NC}"
pip install -r requirements.txt 

# Generate the documentation
while true; do
	echo ""; read -p "$(echo -e "${RED}Do you want to generate the documentation with Doxygen? (y/n)${NC} ")" yn
    	case $yn in
        	[Yy]* ) doxygen Doxyfile; break;;
        	[Nn]* ) exit;;
        	* ) echo -e "${RED}Please answer yes or no.${NC}";;
    	esac
done
