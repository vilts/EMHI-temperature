CREATE TABLE emhi (
    id INTEGER PRIMARY KEY,
    temperature REAL,
    city_id INTEGER,
    timestamp TEXT
);

CREATE TABLE cities (
    id INTEGER PRIMARY KEY,
    regexp TEXT,
    name TEXT
);

INSERT INTO cities (regexp, name) VALUES ('<div style="position: absolute; left: 247px; top: 82px; width:70px; height:13px; color:#993300;" class="kaarditekst">(-?\d+\.?\d+)</div>', 'Tallinn');
INSERT INTO cities (regexp, name) VALUES ('<div style="position: absolute; left: 322px; top: 187px; width:70px; height:13px; color:#993300;" class="kaarditekst">(-?\d+\.?\d+)</div>', 'Türi');
INSERT INTO cities (regexp, name) VALUES ('<div style="position: absolute; left: 418px; top: 279px; width:70px; height:13px; color:#993300;" class="kaarditekst">(-?\d+\.?\d+)</div>', 'Tartu');