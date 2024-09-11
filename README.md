# atproto-nodeinfo-gen

A tool to generate well-known nodeinfo files for atprotocol servers.

# Usage

    usage: atproto-nodeinfo-gen [-h] [-n NAME] [-d DESCRIPTION] [-o OUT] hostname
    
    Generate a well-known nodeinfo file for a PDS.
    
    positional arguments:
      hostname              The hostname of the PDS to generate the file for.
    
    options:
      -h, --help            show this help message and exit
      -n NAME, --name NAME  The name of the PDS.
      -d DESCRIPTION, --description DESCRIPTION
                            The description of the PDS.
      -o OUT, --out OUT     The destination that the well-known data is written to.

Direct CLI:

    $ atproto-nodeinfo-gen -n "My PDS" -d "A PDS for my project" -o /path/to/your/pds/.well-known/nodeinfo my-pds.example.com

Docker:

    $ docker run --rm -v /path/to/your/www/.well-known/:/out ghcr.io/github/atproto-nodeinfo-gen:latest -n "My PDS" -d "A PDS for my project" -o /out/nodeinfo my-pds.example.com

# Deployment

The easiest thing to do is to run the container every 30 minutes using a crontab entry like:

    0,30 * * * * docker run -v /path/to/your/www/.well-known/:/out/ ghcr.io/ngerakines/atproto-nodeinfo-gen:latest my-pds.example.com -o /out/nodeinfo

# Container

The container is built and published to the GitHub Container Registry (ghcr.io/github/atproto-nodeinfo-gen:latest) on every push to the main branch.

