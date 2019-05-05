class Tetris2{

    constructor(canvas){
        this.COLS = 10;
        this.ROWS = 20;
        this.board = [];
        this.lose = false;
        this.interval = null;
        this.intervalRender = null;
        this.current = []; // current moving shape
        this.currentX = 0; // position of current shape
        this.currentY = 0; // position of current shape
        this.freezed = false; // is current shape settled on the board?
        this.shapes = [
            [ 1, 1, 1, 1 ],
            [ 1, 1, 1, 0,
                1 ],
            [ 1, 1, 1, 0,
                0, 0, 1 ],
            [ 1, 1, 0, 0,
                1, 1 ],
            [ 1, 1, 0, 0,
                0, 1, 1 ],
            [ 0, 1, 1, 0,
                1, 1 ],
            [ 0, 1, 0, 0,
                1, 1, 1 ]
        ];
        this.colors = ['cyan', 'orange', 'blue', 'yellow', 'red', 'green', 'purple'];
        this.canvas = canvas;
        this.ctx = this.canvas.getContext( '2d' );
        this.W = 300;
        this.H = 600;
        this.BLOCK_W = this.W / this.COLS;
        this.BLOCK_H = this.H / this.ROWS;
        // this.newGame();
    }

    // clears the board
    init() {
        for ( let y = 0; y < this.ROWS; ++y ) {
            this.board[ y ] = [];
            for ( let x = 0; x < this.COLS; ++x ) {
                this.board[ y ][ x ] = 0;
            }
        }
    }

    // creates a new 4x4 shape in global variable 'current'
    // 4x4 so as to cover the size when the shape is rotated
    newShape() {
        let id = Math.floor( Math.random() * this.shapes.length );
        let shape = this.shapes[ id ]; // maintain id for color filling

        this.current = [];
        for ( let y = 0; y < 4; ++y ) {
            this.current[ y ] = [];
            for ( let x = 0; x < 4; ++x ) {
                let i = 4 * y + x;
                if ( typeof shape[ i ] !== 'undefined' && shape[ i ] ) {
                    this.current[ y ][ x ] = id + 1;
                }
                else {
                    this.current[ y ][ x ] = 0;
                }
            }
        }

        // new shape starts to move
        this.freezed = false;
        // position where the shape will evolve
        this.currentX = 5;
        this.currentY = 0;
    }

    // checks if the resulting position of current shape will be feasible
    valid( offsetX, offsetY, newCurrent ) {
        offsetX = offsetX || 0;
        offsetY = offsetY || 0;
        offsetX = this.currentX + offsetX;
        offsetY = this.currentY + offsetY;
        newCurrent = newCurrent || this.current;

        for ( let y = 0; y < 4; ++y ) {
            for ( let x = 0; x < 4; ++x ) {
                if ( newCurrent[ y ][ x ] ) {
                    if ( typeof this.board[ y + offsetY ] === 'undefined'
                        || typeof this.board[ y + offsetY ][ x + offsetX ] === 'undefined'
                        || this.board[ y + offsetY ][ x + offsetX ]
                        || x + offsetX < 0
                        || y + offsetY >= this.ROWS
                        || x + offsetX >= this.COLS ) {
                        if (offsetY === 1 && this.freezed) {
                            this.lose = true; // lose if the current shape is settled at the top most row
                            document.getElementById('playbutton').disabled = false;
                        }
                        return false;
                    }
                }
            }
        }
        return true;
    }

    // keep the element moving down, creating new shapes and clearing lines
    tick() {
        if ( this.valid(0, 1) ) {
            this.currentY++;
        }
        // if the element settled
        else {
            this.freeze();
            this.valid(0, 1);
            this.clearLines();
            if (this.lose) {
                this.clearAllIntervals();
                return false;
            }
            this.newShape();
        }
    }

    // check if any lines are filled and clear them
    clearLines() {
        for ( let y = this.ROWS - 1; y >= 0; --y ) {
            let rowFilled = true;
            for ( let x = 0; x < this.COLS; ++x ) {
                if ( this.board[ y ][ x ] === 0 ) {
                    rowFilled = false;
                    break;
                }
            }
            if ( rowFilled ) {
                document.getElementById( 'clearsound' ).play();
                for ( let yy = y; yy > 0; --yy ) {
                    for ( let x = 0; x < this.COLS; ++x ) {
                        this.board[ yy ][ x ] = this.board[ yy - 1 ][ x ];
                    }
                }
                ++y;
            }
        }
    }

    // stop shape at its position and fix it to board
    freeze() {
        for ( let y = 0; y < 4; ++y ) {
            for ( let x = 0; x < 4; ++x ) {
                if ( this.current[ y ][ x ] ) {
                    this.board[ y + this.currentY ][ x + this.currentX ] = this.current[ y ][ x ];
                }
            }
        }
        this.freezed = true;
    }

    // returns rotates the rotated shape 'current' perpendicularly anticlockwise
    static rotate(current ) {
        let newCurrent = [];
        for ( let y = 0; y < 4; ++y ) {
            newCurrent[ y ] = [];
            for ( let x = 0; x < 4; ++x ) {
                newCurrent[ y ][ x ] = current[ 3 - x ][ y ];
            }
        }
        return newCurrent;
    }

    newGame() {
        this.clearAllIntervals();
        this.init();
        this.newShape();
        this.lose = false;
        this.intervalRender = setInterval( this.render.bind(this), 30 );
        this.interval = setInterval( this.tick.bind(this), 400 );
    }

    clearAllIntervals(){
        clearInterval( this.interval );
        clearInterval( this.intervalRender );
    }

    keyPress( key ) {
        switch ( key ) {
            case 'left':
                if ( this.valid( -1 ) ) {
                    this.currentX--;
                }
                break;
            case 'right':
                if ( this.valid( 1 ) ) {
                    this.currentX++;
                }
                break;
            case 'down':
                if ( this.valid( 0, 1 ) ) {
                    this.currentY++;
                }
                break;
            case 'rotate':
                let rotated = Tetris.rotate( this.current );
                if ( this.valid( 0, 0, rotated ) ) {
                    this.current = rotated;
                }
                break;
            case 'drop':
                while( this.valid(0, 1) ) {
                    this.currentY++;
                }
                this.tick();
                break;
        }
    }

    // draw a single square at (x, y)
    drawBlock( x, y ) {
        this.ctx.fillRect( this.BLOCK_W * x, this.BLOCK_H * y, this.BLOCK_W - 1 , this.BLOCK_H - 1 );
        this.ctx.strokeRect( this.BLOCK_W * x, this.BLOCK_H * y, this.BLOCK_W - 1 , this.BLOCK_H - 1 );
    }

    // draws the board and the moving shape
    render() {
        this.ctx.clearRect( 0, 0, this.W, this.H );
        this.ctx.strokeStyle = 'black';
        for ( let x = 0; x < this.COLS; ++x ) {
            for ( let y = 0; y < this.ROWS; ++y ) {
                if ( this.board[ y ][ x ] ) {
                    this.ctx.fillStyle = this.colors[ this.board[ y ][ x ] - 1 ];
                    this.drawBlock( x, y );
                }
            }
        }

        this.ctx.fillStyle = 'red';
        this.ctx.strokeStyle = 'black';
        for ( let y = 0; y < 4; ++y ) {
            for ( let x = 0; x < 4; ++x ) {
                if ( this.current[ y ][ x ] ) {
                    this.ctx.fillStyle = this.colors[ this.current[ y ][ x ] - 1 ];
                    this.drawBlock( this.currentX + x, this.currentY + y );
                }
            }
        }
    }
}