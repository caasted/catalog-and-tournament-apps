# Catalog App Project

This project was developed as part of Udacity's Full Stack Web Developer Nanodegree. It utilizes **flask**, **sqlalchemy** and **Google OAuth** to generate a web interface for one or more product catalogs. Authenticated users can create their own store front, while users with the appropriate authorization can create, edit, and delete products within their own store.

## Quickstart

1. Within a running vagrant virtual machine, navigate to `/vagrant/catalog/`.
2. Initialize the supporting database by running `python database_setup.py`.
3. You can populate the database with a sample catalog by running `python database_fill.py`.
4. Run `python project.py` to launch the python webserver.
5. View the web application in your web browser at `http://localhost:8000/`.
6. Login through the link in the top-left and connect using your Google+ account.

If you run these steps in order, the sample store will not be editable because you are not the owner.
If you complete steps 4-6 before step 3, you will then be the owner of the store.

## License

The **/catalog** portion of this repository is free software, and may be redistributed under the terms specified in the [LICENSE](https://github.com/caasted/catalog-and-tournament-apps/blob/master/vagrant/catalog/LICENSE) file.
