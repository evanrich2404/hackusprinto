#!/usr/bin/node
import Phaser from 'phaser';
// Initialize the Phaser game instance
const game = new Phaser.Game({
    type: Phaser.AUTO,
    width: 1200,
    height: 600,
    backgroundColor: '#404040'
});

// Load game assets
game.load.image('cloud', 'images/cloud.png');
game.load.image('raindrop', 'images/raindrop.png');

// Define the Cloud class
class Cloud extends Phaser.GameObjects.Sprite {
    constructor (scene, x, y) {
        super(scene, x, y, 'cloud');
        this.speed = 5;
    };

    update () {
        const cursors = this.scene.input.keyboard.createCursorKeys();
        if (cursors.left.isDown) {
            this.x -= this.speed;
        } else if (cursors.right.isDown) {
            this.x += this.speed;
        };

        if (this.x < 0) {
            this.x = 0;
        } else if (this.x > this.scene.sys.game.config.width) {
            this.x = this.scene.sys.game.config.width;
        };
    };
};

// Define the Raindrop class
class Raindrop extends Phaser.GameObjects.Sprite {
    constructor (scene, x, y) {
        super(scene, x, y, 'raindrop');
        this.speedy = Phaser.Math.Between(3, 7);
    };

    update () {
        this.y += this.speedy;
        if (this.y > this.scene.sys.game.config.height) {
            this.y = Phaser.Math.Between(-100, -40);
            this.x = Phaser.Math.Between(1, this.scene.sys.game.config.width - this.width);
            this.speedy = Phaser.Math.Between(5, 10);
        };
    };
};

// Create game objects and add them to groups
let cloud;
let raindrops;
let allSprites;

game.scene.add('main', {
    create: function () {
        cloud = new Cloud(this, game.config.width / 2, game.config.height - 100);
        raindrops = this.add.group({
            classType: Raindrop,
            runChildUpdate: true
        });
        for (let i = 0; i < 8; i++) {
            const raindrop = raindrops.get();
            raindrop.setActive(true);
            raindrop.setVisible(true);
        };
        allSprites = this.add.group([cloud, raindrops]);
    },

    update: function () {
        cloud.update();
    }
});

// Start the game
game.scene.start('main');
