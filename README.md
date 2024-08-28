## DAFNI SCQUAIR - PyQUANT3
### Repository for geographic visualisations and scnearios in DAFNI SCQUAIR Project
Main repository: [PyQUANT3](https://github.com/maptube/PyQUANT3) <br />
<br />

## Visualisation ##
### File Inputs ###
1. QUANT Impact Statistics 
2. MSOA
    - MSOA shapefile - 2011 England, Wales & Scotland 
    - [Zone codes](https://osf.io/x2gbn/)
3. Geographic boundaries - Bounding Box Coordinates 
    - [England & Wales](https://geoportal.statistics.gov.uk/datasets/980da620a0264647bd679642f96b42c1/explore?location=54.403370%2C-0.937795%2C7.22)
    - [Scotland](https://www.nrscotland.gov.uk/statistics-and-data/geography/our-products/settlements-and-localities-dataset/settlements-and-localities-digital-boundaries)

### Context ###
Python files for visualising impact statistics of road, bus and rail mode generated from PyQUANT3. Outputs include: 
- Choropleth: the mean score of statistics where the particular zone number was used as origin/ destination
- Flow maps: arrows that show the top destination for each origin
- Local flow maps: zoomed in flow maps generated by setting up a bounding box for a specific city/ town

## Scenarios ##
### File Inputs ###
The “scenarios/UK2070” folder is put in the “inputs” directory of PyQUANT3. Individual scenario file can be run with the "--network scenarios/UK2070/xxx/xxx.graphml --mode=2" parameter.

### Context ###
Included case studies are constructed based on the filtered high impact clusters from the CkDiffRail and savedSecsRail choropleths in the Tyne-Tees Cluster. The scenarios add additional nodes to pairs of [existing stations](https://github.com/davwheat/uk-railway-stations) if their distance apart is larger than the threshold. A threshold is set to represent small changes (5 & 10km) and large changes (20 & 30km) scenarios. 

Scenarios:
1. Triangle link connecting Lancaster, Newcastle & Darlington
2. Horizontal (H1) link connecting Mayport to Newcastle
3. Horizontal (H2) link connecting Parton to Seaham
4. Horizontal (H3) link connecting Askam-in-Furness to Middlesbrough - Route 1
5. Horizontal (H4) link connecting Askam-in-Furness to Middlesbrough - Route 2

The geographic presentation of these case studies can be viewed in the “scenarios_qgis” folder:
- _uk_tyne-tees.qgs_
- _Tyne-Tees_stations.shp_: filtered exisitng stations in the Tyne-Tees Cluster
- _Tyne-Tees_impact.shp_: high impact clusters in the Tyne-Tees Cluster (include both CkDiffRail and savedSecsRail)
- _"scenarios" folder_: digtised points of nodes in scenarios 
- _"distance matrix" folder_: distance matrix of all exisiting stations and filtered links that have distance smaller or equal to threshold
- _"impacts" folder_: high impact areas in CkDiffRail and savedSecsRail (filtered from choropleths)
- _"additional" folder_: additional links and points that connect pairs that have distance larger than threshold 
