export class SpatialCore3D {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        this.options = Object.assign({ radius: 65, detail: 2, speed: 0.003 }, options);
        this.init();
    }

    init() {
        this.scene = new THREE.Scene();
        this.camera = new THREE.PerspectiveCamera(40, this.container.clientWidth / this.container.clientHeight, 0.1, 1000);
        this.camera.position.z = 240;

        this.renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
        this.container.appendChild(this.renderer.domElement);

        const geo = new THREE.IcosahedronGeometry(this.options.radius, this.options.detail);
        const mat = new THREE.MeshBasicMaterial({ color: 0xffffff, wireframe: true, transparent: true, opacity: 0.25 });
        this.mesh = new THREE.Mesh(geo, mat);
        this.scene.add(this.mesh);

        const pGeo = new THREE.IcosahedronGeometry(this.options.radius + 7, 3);
        const pMat = new THREE.PointsMaterial({ color: 0x00f0ff, size: 1.8, transparent: true, opacity: 0.6 });
        this.particles = new THREE.Points(pGeo, pMat);
        this.scene.add(this.particles);

        window.addEventListener('resize', () => this.onResize());
    }

    onResize() {
        if (!this.container.clientWidth || !this.container.clientHeight) return;
        this.camera.aspect = this.container.clientWidth / this.container.clientHeight;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
    }

    tick() {
        this.mesh.rotation.y += this.options.speed;
        this.mesh.rotation.x += this.options.speed * 0.3;
        this.particles.rotation.y -= this.options.speed * 0.7;
        this.renderer.render(this.scene, this.camera);
    }
}
