THREE.Object3D.prototype.lookAtWorld = function( vector ) {

    this.parent.worldToLocal( vector );
    this.lookAt( vector );

}

var FONT_SIZE = 5;
var FONT_SIZE_NBR = 3;
var LINK_HEIGHT = 200;

var camera, scene, renderer;
init();
animate();

function init( ) {
    camera = new THREE.PerspectiveCamera( 45, window.innerWidth / window.innerHeight, 1, 10000 );
    camera.position.set( -50, 200, 50 );

    var controls = new THREE.OrbitControls( camera );
    controls.target.set( 0, 200, 0 );
    controls.update();

    scene = new THREE.Scene();
    scene.background = new THREE.Color( 0xf0f0f0 );
//    scene.background = new THREE.Color( 0x000000 );

    setLines();

    // 加载json
    var xhr;
    if(window.XMLHttpRequest){
        xhr = new XMLHttpRequest();
    }else if(window.ActiveXObject){
        xhr = new window.ActiveXObject();
    }else{
        alert("请升级至最新版本的浏览器");
    }
    if(xhr !=null){
        xhr.open("GET","../data/text.json",true);
        xhr.send(null);
        xhr.onreadystatechange=function(){
            if(xhr.readyState==4&&xhr.status==200){
                var obj = JSON.parse(xhr.responseText);
                loadTextGraph(obj);

            }
        };

    }


    renderer = new THREE.WebGLRenderer( { antialias: true } );
    renderer.setPixelRatio( window.devicePixelRatio );
    renderer.setSize( window.innerWidth, window.innerHeight );
    document.body.appendChild( renderer.domElement );
    window.addEventListener( 'resize', onWindowResize, false );

} // end init

var allChars = [];
function loadTextGraph(textJson){
var texts = textJson;
var loader = new THREE.FontLoader();
    loader.load( './FZLanTingHeiS-UL-GB_Regular.json', function ( font ) {
        console.log("font loaded")
        var color = 0x010101;
        var matDark = new THREE.LineBasicMaterial( {
            color: color,
            side: THREE.DoubleSide
        } );

        var matLite = new THREE.MeshBasicMaterial( {
            color: color,
//            transparent: true,
//            opacity: 0.4,
            side: THREE.DoubleSide
        } );

        var makeChar = function(char, material, size, x, y, z){
            var text;
            var textShape = new THREE.BufferGeometry();

            var shapes = font.generateShapes( char, size, 4 );

            var geometry = new THREE.ShapeGeometry( shapes );
            geometry.computeBoundingBox();

            textShape.fromGeometry( geometry );

            text = new THREE.Mesh( textShape, material );
            text.position.y = y || 0;
            text.position.x = x || 0; //i*4*FONT_SIZE;
            text.position.z = z || 0;
            return text;
        }

        var makeLink = function(x1, y1, z1, x2, y2, z2, weight){
            var geometry = new THREE.Geometry();
            geometry.vertices.push( new THREE.Vector3(x1, y1, z1 ) );
            geometry.vertices.push( new THREE.Vector3(x2, y2, z2 ) );
            var line = new THREE.Line( geometry, new THREE.LineBasicMaterial( { color: 0x006699} ) );
            return line;
        }
        var i = 0;
        var current = {}
        var previous = null;
        while(current=texts[i]){
            i ++;
            var currentChar = current['char'];
            var nbrs = current['neighbour'];
            console.log(currentChar)

            var charX = i*6*FONT_SIZE;
            var charObj = makeChar(currentChar, matDark, FONT_SIZE, charX, LINK_HEIGHT)
            scene.add(charObj);
            allChars.push(charObj);

            if(previous){
                var charLinkObj = makeLink(previous.x, previous.y, previous.z, charX, LINK_HEIGHT, 0);
                var charWeightObj = makeChar(previous.weight, matDark, FONT_SIZE/3.0, (previous.x+charX)/2.0, LINK_HEIGHT, 0);
                scene.add(charLinkObj);
                scene.add(charWeightObj);
                allChars.push(charWeightObj);
            }
            previous = {x: charX, y: LINK_HEIGHT, z: 0, weight: current['outWeight']};

            var r = 3*FONT_SIZE;
            var interval =Math.PI * 2 / nbrs.length;
            console.log("#########")
            for(var j=0;j<nbrs.length;j++){
                console.log(nbrs[j][0]);
                var z = r * Math.cos(j*interval);
                var y = r * Math.sin(j*interval) + LINK_HEIGHT;
                console.log(j*interval+" "+nbrs[j][0]+ ":"+z+","+y);
                var nbrObj = makeChar(nbrs[j][0], matLite, FONT_SIZE_NBR, charObj.position.x, y, z);
                scene.add(nbrObj);
                allChars.push(nbrObj);

                var linkNbrObj = makeLink(charObj.position.x, charObj.position.y, charObj.position.z, charObj.position.x, y, z);
                scene.add(linkNbrObj);

                var weightNbrObj = makeChar(nbrs[j][1], matLite, FONT_SIZE_NBR/3.0, charObj.position.x, (charObj.position.y+y)/2.0, (charObj.position.z+z)/2.0);
                scene.add(weightNbrObj);
                allChars.push(weightNbrObj);
            }
        }



    } ); //end load function
}

function setLines(){
    var geometry = new THREE.Geometry();
    geometry.vertices.push( new THREE.Vector3(0, 0, 0 ) );//在x轴上定义两个点p1(-500,0,0)
    geometry.vertices.push( new THREE.Vector3( 1000, 0, 0 ) );//p2(500,0,0)

    for ( var i = 0; i <= 50; i ++ ) {//这两个点决定了x轴上的一条线段，将这条线段复制20次，分别平行移动到z轴的不同位置，就能够形成一组平行的线段。

        var line = new THREE.Line( geometry, new THREE.LineBasicMaterial( { color: 0xaaaaaa, opacity: 0.1} ) );
        line.position.z = ( i * 20 ) - 500;
        scene.add( line );

        var line = new THREE.Line( geometry, new THREE.LineBasicMaterial( { color: 0xaaaaaa, opacity: 0.1 } ) );
        line.position.z += 500;
        line.position.x = ( i * 20 ) ;
        line.rotation.y = 90 * Math.PI / 180; //  旋转90度
        scene.add( line );
//将p1p2这条线先围绕y轴旋转90度，然后再复制20份，平行于z轴移动到不同的位置，也能形成一组平行线。
    }
}


function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize( window.innerWidth, window.innerHeight );
}

function animate() {
    requestAnimationFrame( animate );
    render();
}

function render() {
    if(allChars){
        allChars.forEach(function(geometry){
            geometry.lookAtWorld(camera.getWorldPosition());
        });
//        console.log("face"+allChars.length);
    }else{
//        console.log("none");
    }

    renderer.render( scene, camera );
}