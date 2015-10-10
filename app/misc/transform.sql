-- Transforms AKIndices v1 schema to v2 schema
SELECT t.community_id,
  d.datatype,
  d.model,
  d.modelname,
  d.scenario,
  d.resolution,
  t.year::text,
  json_build_array(
    t.january::decimal(3,1),
    t.february::decimal(3,1),
    t.march::decimal(3,1),
    t.april::decimal(3,1),
    t.may::decimal(3,1),
    t.june::decimal(3,1),
    t.july::decimal(3,1),
    t.august::decimal(3,1),
    t.september::decimal(3,1),
    t.october::decimal(3,1),
    t.november::decimal(3,1),
    t.december::decimal(3,1))::jsonb AS temps
INTO TEMP temp01
FROM temperatures t
INNER JOIN datasets d ON d.id=t.dataset_id;

--------------------------------------------------------------------------------

SELECT community_id,
  datatype,
  model,
  modelname,
  scenario,
  resolution,
  json_object_agg(year, temps)::jsonb AS data
INTO TEMP temp02
FROM temp01
GROUP BY community_id, datatype, model, modelname, scenario, resolution;

--------------------------------------------------------------------------------

CREATE TEMP SEQUENCE a;
SELECT nextval('a') AS id,
  community_id,
  json_build_object(
    'datatype', datatype,
    'model', model,
    'modelname', modelname,
    'scenario', scenario,
    'resolution', resolution)::jsonb as dataset,
  data
INTO TEMP temp03
FROM temp02;

--------------------------------------------------------------------------------

WITH all_json_key_value AS (
  SELECT id, community_id, t1.key, t1.value
  FROM temp03, jsonb_each(dataset) AS t1
  UNION
  SELECT id, community_id, t1.key, t1.value
  FROM temp03, jsonb_each(data) AS t1
)
SELECT community_id, json_object_agg(key, value) AS data
INTO TEMP temp04
GROUP BY id, community_id;

--------------------------------------------------------------------------------

SELECT community_id, json_agg(data)::jsonb AS data
INTO TEMP temp05
FROM temp04
GROUP BY community_id;

--------------------------------------------------------------------------------

SELECT c.name, c.latitude, c.longitude, c.northing, c.easting, t.data
INTO new_communities
FROM temp05 t
INNER JOIN communities c ON c.id=t.community_id;















select distinct on (doc->'model', doc->'datatype', doc->'scenario') doc->'model', doc->'datatype', doc->'scenario' from new_communities c, jsonb_array_elements(c.data) with ordinality t1(doc, rn);
