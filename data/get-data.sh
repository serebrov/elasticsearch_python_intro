#!/usr/bin/env bash
set -e
SCRIPT_PATH=`dirname $0`

# Download all countries data
wget --continue http://download.geonames.org/export/dump/allCountries.zip
unzip -o allCountries.zip

pushd $SCRIPT_PATH

echo "Filtering the geo data..."
# Filter all data to keep only the geo objects we want to have
cat allCountries.txt | 
awk '
    BEGIN { FS="\t" }
    $18 ~ /Europe.+/ { print }
' | awk '
    BEGIN { FS="\t" }
    $7 "." $8 ~ "H.FISH"  ||  #  fishing area	a fishing ground, bank or area where fishermen go to catch fish
    $7 "." $8 ~ "H.FLLS"  ||  #  waterfall(s)	a perpendicular or very steep descent of the water of a stream
    $7 "." $8 ~ "H.GYSR"  ||  #  geyser	a type of hot spring with intermittent eruptions of jets of hot water and steam
    $7 "." $8 ~ "H.LGN"   ||  #  lagoon	a shallow coastal waterbody, completely or partly separated from a larger body of water by a barrier island, coral reef or other depositional feature
    $7 "." $8 ~ "H.LK"    ||  #  lake	a large inland body of standing water
    $7 "." $8 ~ "H.PND"   ||  #  pond	a small standing waterbody
    $7 "." $8 ~ "H.POOL"  ||  #  pool(s)	a small and comparatively still, deep part of a larger body of water such as a stream or harbor; or a small body of standing water
    $7 "." $8 ~ "H.RSV"   ||  #  reservoir(s)	an artificial pond or lake
    $7 "." $8 ~ "H.SPNG"  ||  #  spring(s)	a place where ground water flows naturally out of the ground
    $7 "." $8 ~ "H.SPNT"  ||  #  hot spring(s)	a place where hot ground water flows naturally out of the ground
    $7 "." $8 ~ "H.WHRL"  ||  #  whirlpool	a turbulent, rotating movement of water in a stream
    $7 "." $8 ~ "L.AMUS"  ||  #  amusement park	Amusement Park are theme parks, adventure parks offering entertainment, similar to funfairs but with a fix location
    $7 "." $8 ~ "L.BTL"   ||  #  battlefield	a site of a land battle of historical importance
    $7 "." $8 ~ "L.PRK"   ||  #  park	an area, often of forested land, maintained as a place of beauty, or for recreation
    $7 "." $8 ~ "L.PRT"   ||  #  port	a place provided with terminal and transfer facilities for loading and discharging waterborne cargo or passengers, usually located in a harbor
    $7 "." $8 ~ "L.RGNH"  ||  #  historical region	a former historic area distinguished by one or more observable physical or cultural characteristics
    # Exclude P.PPL, we load the cities separately from the cities15000.txt
    # $7 "." $8 ~ "P.PPL" ||  #  populated place	a city, town, village, or other agglomeration of buildings where people live and work
    $7 "." $8 ~ "S.AMTH"  ||  #  amphitheater	an oval or circular structure with rising tiers of seats about a stage or open space
    $7 "." $8 ~ "S.ANS"   ||  #  archaeological/prehistoric site	a place where archeological remains, old structures, or cultural artifacts are located
    $7 "." $8 ~ "S.ART"   ||  #  piece of art	a piece of art, like a sculpture, painting. In contrast to monument (MNMT) it is not commemorative.
    $7 "." $8 ~ "S.CAVE"  ||  #  cave(s)	an underground passageway or chamber, or cavity on the side of a cliff
    $7 "." $8 ~ "S.CSTL"  ||  #  castle	a large fortified building or set of buildings
    $7 "." $8 ~ "S.CTRS"  ||  #  space center	a facility for launching, tracking, or controlling satellites and space vehicles
    $7 "." $8 ~ "S.FT"    ||  #  fort	a defensive structure or earthworks
    $7 "." $8 ~ "S.HSTS"  ||  #  historical site	a place of historical importance
    $7 "." $8 ~ "S.LTHSE" ||  #  lighthouse	a distinctive structure exhibiting a major navigation light
    $7 "." $8 ~ "S.MNMT"  ||  #  monument	a commemorative structure or statue
    $7 "." $8 ~ "S.MUS"   ||  #  museum	a building where objects of permanent interest in one or more of the arts and sciences are preserved and exhibited
    $7 "." $8 ~ "S.OBPT"  ||  #  observation point	a wildlife or scenic observation point
    $7 "." $8 ~ "S.PAL"   ||  #  palace	a large stately house, often a royal or presidential residence
    $7 "." $8 ~ "S.PYR"   ||  #  pyramid	an ancient massive structure of square ground plan with four triangular faces meeting at a point and used for enclosing tombs
    $7 "." $8 ~ "S.RUIN"  ||  #  ruin(s)	a destroyed or decayed structure which is no longer functional
    $7 "." $8 ~ "S.THTR"  ||  #  theater	A building, room, or outdoor structure for the presentation of plays, films, or other dramatic performances
    $7 "." $8 ~ "S.UNIV"  ||  #  university	An institution for higher learning with teaching and research facilities constituting a graduate school and professional schools that award master degrees and doctorates and an undergraduate division that awards bachelor degrees.
    $7 "." $8 ~ "S.ZOO"   ||  #  zoo	a zoological garden or park where wild animals are kept for exhibition
    $7 "." $8 ~ "T.BCH"   ||  #  beach	a shore zone of coarse unconsolidated sediment that extends from the low-water line to the highest reach of storm waves
    $7 "." $8 ~ "T.CNYN"  ||  #  canyon	a deep, narrow valley with steep sides cutting into a plateau or mountainous area
    $7 "." $8 ~ "-----"   { print }  # The ---- pattern is just to structure the code nicely, there is no such feature code
' > geoObjects.txt

echo 'Done'
ls -lah allCountries.txt
ls -lah geoObjects.txt

popd
