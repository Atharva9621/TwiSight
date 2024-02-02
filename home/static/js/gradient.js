const canvas = document.getElementById('canvas1')
const c = canvas.getContext('2d')
canvas.width = window.innerWidth//1024
canvas.height = window.innerHeight //576

colors = [
    {r: 145, g: 174, b: 227},
    {r: 223, g:200, b:162},
    {r: 220, g: 200, b: 255},
    {r: 250, g:200, b:220},
    {r: 190, g: 240, b: 210},
    {r: 225, g:160, b:132},
]

class GlowParticle {
    constructor(x, y, radius, rgb, effect){
        this.x = x;
        this.y = y;
        this.radius = radius;
        this.rgb = rgb;
        this.effect = effect;

        this.vx = Math.random() - 0.5
        this.vy = Math.random() - 0.5

        this.sinValue = Math.random()
        this.weight = 1

        if(this.vx>0)this.vx+=0.1;
        else this.vx-=0.1;
        if(this.vy>0)this.vy+=0.1;
        else this.vy -= 0.1;
    }
    draw(context){
        context.beginPath();
        const g = context.createRadialGradient(
            this.x,
            this.y,
            this.radius * 0.01,
            this.x,
            this.y,
            this.radius
        );
        g.addColorStop(0,   `rgba(${this.rgb.r}, ${this.rgb.g}, ${this.rgb.b}, 1)`);
        g.addColorStop(1,   `rgba(${this.rgb.r}, ${this.rgb.g}, ${this.rgb.b}, 0)`);
        context.fillStyle = g;
        context.arc(this.x, this.y, this.radius, 0, Math.PI*2);
        context.fill();
    }
    update(){
        this.radius += Math.sin(this.sinValue)*this.weight
        this.sinValue += 0.01
        if(this.x > this.effect.width-this.radius || this.x < this.radius)this.vx*=-1;
        if(this.y > this.effect.height-this.radius || this.y < this.radius)this.vy*=-1;

        this.x+=this.vx;
        this.y+=this.vy;
    }
}

class Effect {
    constructor(canvas, context){
        this.pixelRatio = (window.devicePixelRatio > 1)? 2: 1;
        this.canvas = canvas;
        this.width = this.canvas.width;
        this.height = this.canvas.height;
        this.particles = [];
        this.numberOfParticles = 50;
        this.maxRadius = 100
        this.minRadius = 40

        this.createParticles()

        this.mouse = {
            x: 0,
            y: 0,
            pressed: false,
            radius: 150
        }
        canvas.globalCompositionOperation = 'saturation'
        window.addEventListener('mousemove', e=>{
            this.mouse.x = e.x;
            this.mouse.y = e.y;
        });
        window.addEventListener('mousedown', e=>{
            this.mouse.pressed = true;
        });
        window.addEventListener('mouseup', e=>{
            this.mouse.pressed = false;
        });
    }
    createParticles(){
        this.particles = []
        const MAX_BASE_RADIUS = 20
        console.log(this.minRadius)
        for(let i=0; i<this.numberOfParticles; i++){
            this.particles.push(new GlowParticle(Math.random()*this.width,
            Math.random()*this.height,
            // Math.random()*MAX_BASE_RADIUS,
            this.minRadius+Math.random()*(this.maxRadius-this.minRadius),
            colors[i%colors.length],
            this))
        }
    }
    handleParticles(context){
        this.particles.forEach((particle)=>{
            particle.draw(context)
            particle.update()
        })
    }
}

const effect = new Effect(canvas, c);
function animate(){
    window.requestAnimationFrame(animate)
    c.fillStyle = 'white'
    c.fillRect(0, 0, canvas.width, canvas.height)
    c.restore() 
    //ANIMATE 
    // c.fillStyle = gradient;
    effect.handleParticles(c);
}
animate()