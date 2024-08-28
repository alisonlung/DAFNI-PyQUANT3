## DAFNI SCQUAIR - PyQUANT3
### Repository for geographic visualisations and scnearios in DAFNI SCQUAIR Project
Main repository: [PyQUANT3](https://github.com/maptube/PyQUANT3) <br />
<br />

## Visualisation ##
### File Inputs ###
1. QUANT Impact Statistics 
2. MSOA
    1. MSOA shapefile - 2011 England, Wales & Scotland 
    2. [Zone codes](https://osf.io/x2gbn/)
3. Geographic boundaries - Bounding Box Coordinates 
    1. [England & Wales](https://geoportal.statistics.gov.uk/datasets/980da620a0264647bd679642f96b42c1/explore?location=54.403370%2C-0.937795%2C7.22)
    2. [Scotland](https://www.nrscotland.gov.uk/statistics-and-data/geography/our-products/settlements-and-localities-dataset/settlements-and-localities-digital-boundaries)

### Context ###
1. Choropleth
2. Flow maps
3. Local flow maps  

## Scenarios ##
### File Inputs ###
The “scenarios” folder is put in the “inputs” directory of PyQUANT3. Individual scenario file can be run with the "--network scenarios/UK2070/xxx/xxx.graphml --mode=2" parameter.

### Context ###
Included case studies are constructed based on the filtered high impact clusters from the CkDiffRail and savedSecsRail choropleths in the Tyne-Tees Cluster. The scenarios add additional nodes to pairs of [existing stations](https://github.com/davwheat/uk-railway-stations) which their distance apart is larger than the threshold. Thresholds are set to represent small changes (5 & 10km) and large changes (20 & 30km) scenarios. 

Scenarios:
1. Triangle connecting Lancaster, Newcastle & Darlington
2. Horizontal (H1) connecting Mayport to Newcastle
3. Horizontal (H2) connecting Parton to Seaham
4. Horizontal (H3) connecting Askam-in-Furness to Middlesbrough - Route 1
5. Horizontal (H4) connecting Askam-in-Furness to Middlesbrough - Route 2

The geographic presentation of these case studies can be viewed in the “scenarios_qgis” folder:
- uk_tyne-tees.qgs
- Tyne-Tees_stations.shp: Filtered exisitng stations in the Tyne-Tees Cluster
- Tyne-Tees_impact.shp: High impact clusters in the Tyne-Tees Cluster (include both CkDiffRail and savedSecsRail)
- "scenarios" folder: digtised points of nodes in scenarios 
- "distance matrix" folder: distance matrix of all exisiting stations and filtered links that have distance smaller or equal to threshold 
- "additional" folder: additional links and points that connect pairs that have distance larger than threshold 