from app import db
from sqlalchemy.sql import text
from flask import abort


class DB:
    @classmethod
    def getCommunity(cls, id):
        cmd = """
            SELECT id, name, latitude, longitude, northing, easting
            FROM new_communities
            WHERE id=:id;
            """
        result = db.engine.execute(text(cmd), id=id).fetchone()
        return result or abort(500)

    @classmethod
    def getCommunities(cls):
        cmd = """
            SELECT id, name
            FROM new_communities
            ORDER BY name ASC;
            """
        result = db.engine.execute(text(cmd), id=id).fetchall()
        return result or abort(500)

    @classmethod
    def getDatasets(cls):
        cmd = """
            SELECT DISTINCT ON (
                doc->'datatype',
                doc->'resolution',
                doc->'modelname',
                doc->'scenario'
            )
                doc->'datatype' AS datatype,
                doc->'resolution' AS resolution,
                doc->'modelname' AS modelname,
                doc->'scenario' AS scenario
            FROM new_communities c,
                jsonb_array_elements(c.data)
                WITH ORDINALITY t1(doc, rn)
            ORDER BY datatype ASC, modelname ASC, scenario ASC;
            """
        result = db.engine.execute(text(cmd)).fetchall()
        return result or abort(500)

    @classmethod
    def getTemps(cls, start, end, community_id, modelname, scenario):
        years = [str(x) for x in range(int(start), int(end)+1)]
        cmd = """
            WITH x AS (
                SELECT name, jsonb_array_elements(data) AS data
                FROM new_communities
                WHERE id=:community_id)
            SELECT d.key AS year, d.value AS temperatures
            FROM x, jsonb_each(data) d
            WHERE data->>'modelname'=:modelname
            AND data->>'scenario'=:scenario
            AND d.key IN :years;
            """
        result = db.engine.execute(text(cmd),
                                   community_id=community_id,
                                   modelname=modelname,
                                   scenario=scenario,
                                   years=tuple(years)).fetchall()
        return result or abort(500)
