import Feature from 'ol/Feature';
import Map from 'ol/Map';
// import Point from 'ol/geom/Point';
import { LineString, Point } from 'ol/geom';
import View from 'ol/View';
import { Circle as CircleStyle, Stroke, Style, Text, Icon, Fill } from 'ol/style';
import { OSM, Vector as VectorSource } from 'ol/source';
import { Tile as TileLayer, Vector as VectorLayer } from 'ol/layer';
import { easeOut } from 'ol/easing';
import { fromLonLat } from 'ol/proj';
import { getVectorContext } from 'ol/render';
import { unByKey } from 'ol/Observable';
import { datasource } from './map';
import { unigram } from './unigram';
import { bigram } from './bigram_csvjson';
import {
  DragRotateAndZoom,
  defaults as defaultInteractions,
} from 'ol/interaction';
import { FullScreen, defaults as defaultControls } from 'ol/control';
// import RoomSharpIcon from '@mui/icons-material/RoomSharp'

let x1, x0, y0, y1, lonlat0, lonlat1;


// This is for making the world map
const tileLayer = new TileLayer({
  source: new OSM({
    wrapX: false,
  }),
});


// This function is to make points and label them
function addRandomFeature(data, name) {
  // console.log(name)
  const geom = new Point(fromLonLat(data));
  const feature = new Feature(geom);

  const iconStyle = new Style({
    // image: new Icon({
    //   anchor: [0.5, 1],
    //   src: 'https://image.shutterstock.com/image-vector/pin-icon-vector-location-map-260nw-1487463347.jpg',
    //   size: [10, 20],
    // }),
    text: new Text({
      textBaseline: 'top',
      text: 'corpus',
      font: 'bold 10px Calibri,sans-serif',
      fill: new Fill({
        color: 'black',
      }),
      stroke: new Stroke({
        color: 'white',
        width: 1,
      }),
    }),
  });

  const pointStyle = new Style({
    image: new CircleStyle({
      radius: 7,
      fill: new Fill({
        color: 'black',
      }),
      stroke: new Stroke({
        color: 'white',
        width: 1,
      }),
    }),
  });

  source.addFeature(feature);
  vector.setStyle([iconStyle, pointStyle])
}


// This is used to make line between two points
function makeLine(data1, data2) {
  var points = [fromLonLat(data1), fromLonLat(data2)];
  var point = new LineString(points)
  var line_feat1 = new Feature(point);

  var lineStyle = new Style({
    stroke: new Stroke({
      color: "black",
      width: 1,
      lineDash: [4, 4, 4],
      lineCap: "butt"
    })
  });

  line_vsrc.addFeature(line_feat1);
  veclay_line.setStyle([lineStyle]);

}

var line_vsrc = new VectorSource({
  wrapX: false
});

var veclay_line = new VectorLayer({
  source: line_vsrc
});

const source = new VectorSource({
  wrapX: false,
});
const vector = new VectorLayer({
  source: source,
});


const map = new Map({
  controls: defaultControls().extend([new FullScreen()]),
  interactions: defaultInteractions().extend([new DragRotateAndZoom()]),
  layers: [tileLayer, veclay_line, vector],
  target: 'map',
  view: new View({
    center: [0, 0],
    zoom: 3,
    multiWorld: true
  }),
});

source.on('addfeature', function (e) {
  map.render()
});


function mapping(name) {// This for loop is used to map all the data of the unigram, bigram, trigram
  for (let j = 0; j < name.length; j++) {
    // instead of datasource.length there will be corpus.length

    if (name[j].Dot_Product >= 0.88) {

      // console.log(unigram[j].Language1)
      let corpname1 = name[j].Language1.toLowerCase();
      let corpname2 = name[j].Language2.toLowerCase();

      for (let i = 0; i < datasource.length; i++) {

        if (datasource[i].corpus === corpname1) {
          // inplace of hindi it will be corpus[j][0]
          x0 = datasource[i].longitude;
          y0 = datasource[i].latitude;
          lonlat0 = [x0, y0];
        }
        if (datasource[i].corpus === corpname2) {
          // inplace of african it will be corpus[j][1]

          x1 = datasource[i].longitude;
          y1 = datasource[i].latitude;
          lonlat1 = [x1, y1];
        }
      }

      addRandomFeature(lonlat0, corpname1); // here we have to share the first corpus name
      addRandomFeature(lonlat1, corpname2); // here we have to share the second corpus name
      makeLine(lonlat0, lonlat1);
    }
  }
}

mapping(unigram);
// mapping(bigram);
























// const duration = 3000;

// function flash(feature) {
//   const start = Date.now();
//   const flashGeom = feature.getGeometry().clone();
//   const listenerKey = tileLayer.on('postrender', animate);

//   function animate(event) {
//     const frameState = event.frameState;
//     const elapsed = frameState.time - start;
//     if (elapsed >= duration) {
//       unByKey(listenerKey);
//       return;
//     }
//     const vectorContext = getVectorContext(event);
//     const elapsedRatio = elapsed / duration;
//     // radius will be 5 at start and 30 at end.
//     const radius = easeOut(elapsedRatio) * 25 + 5;
//     const opacity = 0;

//     const style = new Style({
//       image: new CircleStyle({
//         radius: 5,
//         stroke: new Stroke({
//           color: 'rgba(255, 0, 0, ' + opacity + ')',
//           width: 0.25,
//         }),
//       }),
//     });

//     vectorContext.setStyle(style);
//     vectorContext.drawGeometry(flashGeom);
//     map.render();
//   }
// }

// // `veclay_line` is the outcome of this complicate code
// /* END: Code for the line joining the 2 points */

// 