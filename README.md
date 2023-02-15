# Install pip3 
# Install python 3.10

# Install virtualenv
```sh
python3 -m pip install --user virtualenv
```

# Create venv folder ( SKIP THIS )
```sh
python3 -m venv venv
```

# SET ENV ( SKIP THIS )
```sh
set VIRTUAL_ENV "$pwd/singhealth-jaundice/venv"
```

# Active ENV 
```sh
# linux
source venv/bin/activate 
# window
.\venv\Scripts\activate
```

# INSTALL package
```sh
  pip3 install opencv-contrib-python
```