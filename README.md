# VK Likes finder

Find posts on vk.com which are marked as liked by some target user.

## Downloading & installation

```bash
git clone --recursive https://github.com/MikeWent/vk-likes-finder.git
cd vk-likes-finder
pip3 install --user --upgrade -r requirements.txt
```

## Updating

```bash
cd vk-likes-finder
git pull
git submodule update --recursive
```

## Via package manager on Linux 

- Ubuntu/Debian: `sudo apt install python3 python3-requests`
- Arch Linux: `sudo pacman -S python python-requests`

### Via [pip](https://pip.pypa.io/en/stable/installing/)

**Don't** do this if you have already installed `requests` via package manager on Linux.

`pip3 install --user --upgrade requests`

## Usage

Simply run the script and follow instructions. Script works with personal token access, so you need to provide working credentials (or access token).

## License

GNU GPLv3
