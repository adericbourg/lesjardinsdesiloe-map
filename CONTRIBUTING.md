# Contribute

This is a static website built with handmade tools. It requires you to have
on your machine:

* Make
* Python 3
* A shell: Linux or MacOS will be fine, you will need WSL on Windows (it
  might work on Cygwin, untested)

## Feed data

All data are defined in the `content` folder.

* `people.yml` is for listing people that attended events
* `reference.yml` is for defining data that seldom change

### People

The only required information in this file is the name.

* To appear on the map, the address (even incomplete) is required
* To appear on the event list, the events are required (the date is
  mandatory)

## Build the website

Enter the development environment by running at the root of this repository:

```shell
source bootstrap.sh
```

Run a local server to have a preview of what you are doing:

```shell
make devserver
```

The local website is available on [http://localhost:9000](http://localhost:9000).
Then, each time you make a change, you should run this command to rebuild the site:

```shell
make dev
```

As a shortcut, you may combine it with:

```shell
make watch
```

This command will rebuild the full site every time you will make a change.

To build and push it for the web (it will override the current version with
your own version):

```shell
make github
```
