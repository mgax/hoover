Hoover is a search tool for large collections of documents. It gues together
proven open-source technologies like elasticsearch and Apache Tika to aid the
work of investigative journalists.

**Documents are imported** from various sources: WebDAV servers, like OwnCloud
and Davros, or datasets prepared in a special metadata-rich ["collectible"
format][collectible].

**Searching** is done through a user-friendly web interface that leverages
Lucene's rich query syntax. Hoover also provides an API to run queries using
the elasticsearch [query DSL][].

[collectible]: https://github.com/mgax/hoover/blob/master/docs/Collectible.md
[query dsl]: https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html


## Installation

Hoover needs Python 3.4 or newer and a running elasticsearch server. You
probably want to set up a [virtualenv][] too.

[virtualenv]: http://docs.python-guide.org/en/latest/dev/virtualenvs/

1. Download the code, install dependencies

   ```shell
   git clone https://github.com/mgax/hoover.git
   cd hoover
   pip install -r requirements.txt
   ```

2. Copy and customize the configuration file

   ```shell
   cp hoover/settings/example_local.py hoover/settings/local.py
   ```

3. Prepare the database and create a Django user

   ```shell
   ./manage.py migrate
   ./manage.py createsuperuser
   ```

4. Run the server

   ```shell
   ./run devserver
   ```

5. Import a collection: first, create the collection in Django admin, at
   http://127.0.0.1:8000/admin/collector/collection/. You need to provide a
   JSON configuration in the "options" field; for the "Monitorul Oficial"
   collection you can use this one:

   ```json
   {"index": "http://mofs.tanker.grep.ro/index.yaml"}
   ```

   Then run the import command. Replace `mof` with your collection name.

   ```shell
   ./manage.py update mof
   ```

6. Run some search queries! There is a minimal search UI on the homepage of the
   Django site (http://127.0.0.1:8000/).


## Development

There is a test suite; run it with `./run tests`.
