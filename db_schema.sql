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

INSERT INTO cities (regexp, name) VALUES ('<div style="position: absolute; left: 247px; top: 82px; width:70px; height:13px; color:#\d+;" class="kaarditekst">(-?\d+\.?\d+)</div>', 'Tallinn');
INSERT INTO cities (regexp, name) VALUES ('<div style="position: absolute; left: 322px; top: 187px; width:70px; height:13px; color:#\d+;" class="kaarditekst">(-?\d+\.?\d+)</div>', 'Türi');
INSERT INTO cities (regexp, name) VALUES ('<div style="position: absolute; left: 418px; top: 279px; width:70px; height:13px; color:#\d+;" class="kaarditekst">(-?\d+\.?\d+)</div>', 'Tartu');
INSERT INTO cities (regexp, name) VALUES ('<div style="position: absolute; left: 241px; top: 251px; width:70px; height:13px; color:#\d+;" class="kaarditekst">(-?\d+\.?\d+)</div>', 'Pärnu');
INSERT INTO cities (regexp, name) VALUES ('<div style="position: absolute; left: 553px; top: 59px; width:70px; height:13px; color:#\d+;" class="kaarditekst">(-?\d+\.?\d+)</div>', 'Narva-Jõesuu');
INSERT INTO cities (regexp, name) VALUES ('<div style="position: absolute; left: 386px; top: 361px; width:70px; height:13px; color:#\d+;" class="kaarditekst">(-?\d+\.?\d+)</div>', 'Valga');
INSERT INTO cities (regexp, name) VALUES ('<div style="position: absolute; left: 339px; top: 257px; width:70px; height:13px; color:#\d+;" class="kaarditekst">(-?\d+\.?\d+)</div>', 'Viljandi');