import React from "react"
import {compose, withProps, withStateHandlers} from "recompose";
import {graphql} from 'gatsby'

import {
    withScriptjs,
    withGoogleMap,
    GoogleMap,
    Marker,
    Polyline,
    InfoWindow,
} from "react-google-maps";
import Layout from "../components/layout"

class MarkerWithInfoWindow extends React.Component {

    constructor() {
        super();
        this.state = {
            isOpen: false
        }
        this.onToggleOpen = this.onToggleOpen.bind(this);
    }

    onToggleOpen() {
        this.setState({
            isOpen: !this.state.isOpen
        });
    }

    render() {
        return (<Marker
            position={this.props.position}
            onClick={this.onToggleOpen}>
            {this.state.isOpen && <InfoWindow onCloseClick={this.onToggleOpen}>
                {/*<h3>{this.props.content}</h3>*/}
                <div>
                    <h6>MMSI {this.props.mmsi}</h6>
                    <h7>Distance Covered {this.props.distance_covered}</h7>
                </div>
            </InfoWindow>}
        </Marker>)
    }
}
const MyMapComponent = compose(
    withStateHandlers(() => ({
        isOpen: false,
    }), {
        onToggleOpen: ({isOpen}) => () => ({
            isOpen: !isOpen,
        })
    }),
    withProps({
        googleMapURL: "https://maps.googleapis.com/maps/api/js?key=AIzaSyDmMZ95xoQ3RB2Bkjd0VnDaFbKv54FEsyI&v=3.exp&libraries=geometry,drawing,places",
        loadingElement: <div style={{height: `100%`}}/>,
        containerElement: <div style={{height: `800px`}}/>,
        mapElement: <div style={{height: `100%`}}/>,
    }),
    withScriptjs,
    withGoogleMap
)((props) =>
    <GoogleMap
        defaultZoom={3}
        defaultCenter={{lat: 9.080000, lng: -79.680000}}
    >
        {
            props.data.allVessel.nodes.map(function (item, i) {
                return (<MarkerWithInfoWindow
                        position={{ lat: item.last_known.lat, lng: item.last_known.lng }}
                        mmsi={item.mmsi}
                        distance_covered={item.distance_km}
                    />
                )
            })
        }
        {
            props.data.allVessel.nodes.map(function (item, i) {
                return (<Polyline
                    key={i}
                    path={item.positions}
                    geodesic={true}
                    options={{
                        strokeColor: '#' + ('000000' + Math.floor(Math.random() * 0xFFFFFF).toString(16)).substr(-6),
                        strokeWeight: 4,
                        icons: [
                            {
                                offset: "0",
                                repeat: "20px"
                            }
                        ]
                    }}
                />)
            })
        }
    </GoogleMap>
)


const IndexPage = (props) => (
    <Layout>
        <div style={{maxWidth: `100%`}}>
            <MyMapComponent data={props.data}/>
        </div>
    </Layout>
)


export default IndexPage
export const query = graphql`
  {
      allVessel {
        nodes {
          mmsi
          positions {
            lat
            lng
          }
          last_known {
            lat
            lng
          }
          distance_km
          num_positions
        }
        totalCount
      }
    }
`
