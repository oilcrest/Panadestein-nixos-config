#-----------------------------
#    _   _ _       ___  ____  
#   | \ | (_)_  __/ _ \/ ___| 
#   |  \| | \ \/ / | | \___ \ 
#   | |\  | |>  <| |_| |___) |
#   |_| \_|_/_/\_\\___/|____/ 
#
#      Panadestein's NixOS
#-----------------------------

{ config, pkgs, inputs, ... }:
{
  imports =
    [
      # Hardware of current machine
      ./hardware-configuration.nix
    ];

  # Overlays
  nixpkgs.overlays = [
    # Emacs overlay
    (import inputs.emacs-overlay)
  ];

  # Nixpkgs configuration
  nixpkgs.config = {
    allowUnfree = true;
    packageOverrides = pkgs: {
      inxi = pkgs.inxi.override { withRecommends = true; };
    };
  };

  # Nix configuration
  nix = {
    settings = {
      substituters = [
        "https://nix-community.cachix.org/"
        "https://cache.nixos.org/"
      ];
      trusted-public-keys = [
        "nix-community.cachix.org-1:mB9FSh9qf2dCimDSUo8Zy7bkq5CX+/rkCWyvRCYg3Fs="
      ];
      trusted-users = [
        "root"
        "loren"
      ];
      experimental-features = [ "nix-command" "flakes" ];
    };
  };

  # Use the latest linux kernel
  boot.kernelPackages = pkgs.linuxPackages_latest;

  # Load AMD CPU microcode
  hardware.cpu.amd.updateMicrocode = true;

  # Add HiDPI support
  hardware.video.hidpi.enable = true;

  # Kernel parameters and modules
  boot.initrd.kernelModules = [ "amdgpu" "hid-apple"];
  boot.kernelParams = [
    "quiet"
    "loglevel=3"
    "rd.systemd.show_status=auto"
    "rd.udev.log_level=3"
    "hid_apple.fnmode=0"
  ];
  boot.initrd.verbose = false;
  boot.plymouth.enable = true;

  # Use the systemd-boot EFI boot loader.
  boot.loader = {
    systemd-boot.enable = false;
    efi.canTouchEfiVariables = true;
    grub.enable = true;
    grub.efiSupport = true;
    grub.device = "nodev";
  };

  # Set hostname
  networking.hostName = "cyrus";

  # Set your time zone.
  time.timeZone = "Europe/Berlin";

  # Set zsh as default shell
  programs.zsh.enable = true;
  users.defaultUserShell = pkgs.zsh;

  # Enable fish shell
  programs.fish.enable = true;

  # Network configuration
  networking = {
    useDHCP = false;
    interfaces.enp2s0f0.useDHCP = true;
    interfaces.enp5s0.useDHCP = true;
    networkmanager.enable = true;
  };
  programs.nm-applet.enable = true;

  # Select internationalisation properties.
  i18n.defaultLocale = "en_US.UTF-8";
  console = {
    font = "Lat2-Terminus16";
    keyMap = "us";
  };

  # Enable the X11 windowing system.
  services.xserver.enable = true;

  # Configure AMD graphics
  services.xserver.videoDrivers = [ "amdgpu" ];
  hardware.opengl.driSupport = true;
  hardware.opengl.extraPackages = with pkgs; [
    amdvlk
  ];
  services.xserver.deviceSection = ''Option "TearFree" "true"'';

  # Display manager
  services.xserver.displayManager = {
    defaultSession = "none+qtile";
    gdm = {
      enable = false;
      wayland = false;
    };
    lightdm = {
      enable = true;
      greeters.enso = {
        enable = true;
      }; 
    };
  };

  # Window managers
  services.xserver.windowManager = {
    xmonad = {
      enable = true;
      enableContribAndExtras = true;
      extraPackages = haskellPackages: [
        haskellPackages.xmonad
        haskellPackages.xmonad-contrib
        haskellPackages.xmonad-extras
      ];
    };
    qtile = {
      enable = true;
    };
  };

  # Desktop environment
  services.xserver.desktopManager.gnome.enable = false;

  # Configure keymap in X11
  services.xserver.layout = "us,de";
  services.xserver.xkbVariant = "altgr-intl";

  # Enable CUPS to print documents.
  services.printing = {
    enable = true;
    clientConf = ''
      ServerName cpcs04.chm.tu-dresden.de 
    '';
    drivers = [ pkgs.epson-workforce-635-nx625-series ];
  };
  services.avahi.enable = true;
  services.avahi.nssmdns = true;

  # Enable sound.
  sound.enable = true;
  hardware.pulseaudio.enable = true;
  hardware.pulseaudio.package = pkgs.pulseaudioFull;
  nixpkgs.config.pulseaudio = true;
  sound.mediaKeys.enable = true;

  # Bluetooth support
  hardware.bluetooth = {
    enable = true;
  };
  services.blueman.enable = true;

  # Enable touchpad support
  services.xserver.libinput = {
    enable = true;
    touchpad = {
      tapping = true;
      naturalScrolling = true;
      scrollMethod = "twofinger";
    };
  };

  # User account and configuration
  users.users.loren = {
    isNormalUser = true;
    home = "/home/loren";
    createHome = true;
    extraGroups = [ "wheel"
                    "audio"
                    "input"
                    "networkmanager" 
                    "systemd-journal" 
                    "video"];
  };

  # Global packages, minimal to avoid polluting environment
  environment.systemPackages = with pkgs; [
    # General utilities
    acpi
    binutils
    cacert
    coreutils
    curl
    dmidecode
    file
    git
    inxi
    killall
    libtool
    pavucontrol
    pciutils
    rsync
    sshfs
    unrar
    unzip
    usbutils
    wget
    which
    # Terminal and CLI utilities
    zsh
    # Text editors and office
    emacsGit
    vim_configurable
    # Programming languages
    gfortran
    qt6.full
    (let
      my-python-packages = python-packages: with python-packages; [
        # Language server protocol
        python-lsp-server
        # Scientific libraries
        ipython
        ipykernel
        jupyter
        matplotlib
        mpmath
        numpy
        pandas
        seaborn
        scikit-learn
        scipy
        sympy
        # Qt backend
        pyqt6
        # Documentation
        sphinx
        # Linters
        autopep8
        flake8
        jedi
        pydocstyle
        pylint
        # Web
        tornado
        # Hy utilities
        hy
        # Misc
        watermark
      ];
      python-with-my-packages = python3.withPackages my-python-packages;
    in
      python-with-my-packages)
    (hy.withPackages (py-packages: with py-packages; [
      # Scientific libraries
      numpy
      matplotlib
      pandas
      scipy
      sympy
      # Qt backend
      pyqt6
    ]))
  ];
  
  # Emacs configuration
  services.emacs = {
    enable = true;
    package = pkgs.emacsGit;
    defaultEditor = true;
  };

  # Enable Java
  programs.java.enable = true;

  # Use Flatpak, just in case
  services.flatpak.enable = true;
  xdg.portal.enable = true;
  xdg.portal.extraPortals = [ pkgs.xdg-desktop-portal-gtk ];

  # Fonts
  fonts.fonts = with pkgs; [
    dina-font
    fira-code
    fira-code-symbols
    font-awesome
    liberation_ttf
    noto-fonts
    noto-fonts-cjk
    noto-fonts-emoji
    proggyfonts
    source-code-pro
    (nerdfonts.override { fonts = [ "SourceCodePro" ]; })
  ];

  # Gnome apps configuration
  programs.dconf.enable = true;
  environment.gnome.excludePackages = (with pkgs; [
    gnome-tour
  ]) ++ (with pkgs.gnome; [
    cheese
    gnome-music
  ]);

  # Gnupg configuration
  programs.gnupg.agent = {
    enable = true;
    enableSSHSupport = true;
  };

  # Enable docker (rarely needed but still)
  virtualisation.docker.enable = true;

  # Additional services
  services.actkbd.enable = true;
  services.gvfs.enable = true;
  services.openssh.enable = true;
  services.teamviewer.enable = true;
  services.upower.enable = true;
  services.gnome.gnome-keyring.enable = true;
  services.dbus = {
    enable = true;
    packages = [ pkgs.dconf ];
  };
  systemd.user.services.maestral = {
    description = "Maestral";
    wantedBy = [ "graphical-session.target" ];
    serviceConfig = {
      ExecStart = "${pkgs.maestral-gui}/bin/maestral_qt";
      Restart = "on-failure";
      PrivateTmp = true;
      ProtectSystem = "full";
      Nice = 10;
    };
  };

  # State version
  system.stateVersion = "22.11";
}