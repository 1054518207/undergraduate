class Tetris {

    constructor(canvas, socket) {
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
        // https://wiki.botzone.org.cn/index.php?title=Tetris 方块对应形状
        this.shapes = [
            [1, 1, 1, 0, 1],
            [1, 1, 1, 0, 0, 0, 1],
            [0, 1, 1, 0, 1, 1],
            [1, 1, 0, 0, 0, 1, 1],
            [0, 1, 0, 0, 1, 1, 1],
            [1, 1, 1, 1],
            [1, 1, 0, 0, 1, 1]
        ];
        this.colors = ['cyan', 'orange', 'blue', 'yellow', 'red', 'green', 'purple'];
        this.canvas = canvas;
        this.ctx = this.canvas.getContext('2d');
        this.W = 300;
        this.H = 600;
        this.BLOCK_W = this.W / this.COLS;
        this.BLOCK_H = this.H / this.ROWS;
        this.socket = socket;
        this.record = [];
        this.blockid = -1;    //存放当前方块ID
        this.model = 0;     //存放当前方块形状
        this.socket.onmessage = (data) =>{
            data = JSON.parse(data['data']);
            let center = data['center'];
            let station = data['station'];
            let x = center[1];
            let y = center[0];
            console.log(center,station);
            switch (this.blockid) {
                case 0:
                    this.forwardToPos(this.transL(x,y,station));
                    break;
                case 1:
                    this.forwardToPos(this.transJ(x,y,station));
                    break;
                case 2:
                    this.forwardToPos(this.transS(x,y,station));
                    break;
                case 3:
                    this.forwardToPos(this.transZ(x,y,station));
                    break;
                case 4:
                    this.forwardToPos(this.transT(x,y,station));
                    break;
                case 5:
                    this.forwardToPos(this.transI(x,y,station));
                    break;
                case 6:
                    this.forwardToPos(this.transO(x,y,station));
                    break;
                default:
                    break;
            }
        }
    }

    // clears the board
    init() {
        for (let y = 0; y < this.ROWS; ++y) {
            this.board[y] = [];
            for (let x = 0; x < this.COLS; ++x) {
                this.board[y][x] = 0;
            }
        }
    }

    // creates a new 4x4 shape in global variable 'current'
    // 4x4 so as to cover the size when the shape is rotated
    // 当需要生成方块时使用
    newShape() {
        let id = Math.floor(Math.random() * this.shapes.length);
        // let id = 6;
        let shape = this.shapes[id]; // maintain id for color filling

        this.record.push(id);
        this.current = [];

        for (let y = 0; y < 4; ++y) {
            this.current[y] = [];
            for (let x = 0; x < 4; ++x) {
                let i = 4 * y + x;
                if (typeof shape[i] !== 'undefined' && shape[i]) {
                    this.current[y][x] = id + 1;
                } else {
                    this.current[y][x] = 0;
                }
            }
        }

        // 尝试返回数组形式
        let jsonData = {
            "blockId": id,
            "matrix": this.board
        };
        this.blockid = id;
        this.model = 0;

        // new shape starts to move
        this.freezed = false;
        // position where the shape will evolve
        this.currentX = 0;
        this.currentY = 0;
        this.socket.send(JSON.stringify(jsonData));
    }

    // checks if the resulting position of current shape will be feasible
    valid(offsetX, offsetY, newCurrent) {
        offsetX = offsetX || 0;
        offsetY = offsetY || 0;
        offsetX = this.currentX + offsetX;
        offsetY = this.currentY + offsetY;
        newCurrent = newCurrent || this.current;

        for (let y = 0; y < 4; ++y) {
            for (let x = 0; x < 4; ++x) {
                if (newCurrent[y][x]) {
                    if (typeof this.board[y + offsetY] === 'undefined'
                        || typeof this.board[y + offsetY][x + offsetX] === 'undefined'
                        || this.board[y + offsetY][x + offsetX]
                        || x + offsetX < 0
                        || y + offsetY >= this.ROWS
                        || x + offsetX >= this.COLS) {
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
        if (this.valid(0, 1)) {
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
        for (let y = this.ROWS - 1; y >= 0; --y) {
            let rowFilled = true;
            for (let x = 0; x < this.COLS; ++x) {
                if (this.board[y][x] === 0) {
                    rowFilled = false;
                    break;
                }
            }
            if (rowFilled) {
                document.getElementById('clearsound').play();
                for (let yy = y; yy > 0; --yy) {
                    for (let x = 0; x < this.COLS; ++x) {
                        this.board[yy][x] = this.board[yy - 1][x];
                    }
                }
                ++y;
            }
        }
    }

    // stop shape at its position and fix it to board
    freeze() {
        for (let y = 0; y < 4; ++y) {
            for (let x = 0; x < 4; ++x) {
                if (this.current[y][x]) {
                    this.board[y + this.currentY][x + this.currentX] = this.current[y][x];
                }
            }
        }
        this.freezed = true;
    }

    // returns rotates the rotated shape 'current' perpendicularly anticlockwise
    static rotate(current) {
        let newCurrent = [];
        for (let y = 0; y < 4; ++y) {
            newCurrent[y] = [];
            for (let x = 0; x < 4; ++x) {
                newCurrent[y][x] = current[3 - x][y];
            }
        }
        return newCurrent;
    }

    newGame() {
        this.clearAllIntervals();
        this.init();
        this.newShape();
        this.lose = false;
        this.intervalRender = setInterval(this.render.bind(this), 40);
        this.interval = setInterval(this.tick.bind(this), 400);
    }

    clearAllIntervals() {
        clearInterval(this.interval);
        clearInterval(this.intervalRender);
    }

    keyPress(key) {
        switch (key) {
            case 'left':
                if (this.valid(-1)) {
                    this.currentX--;
                }
                break;
            case 'right':
                if (this.valid(1)) {
                    this.currentX++;
                }
                break;
            case 'down':
                if (this.valid(0, 1)) {
                    this.currentY++;
                }
                break;
            case 'rotate':
                let rotated = Tetris.rotate(this.current);
                if (this.valid(0, 0, rotated)) {
                    this.current = rotated;
                }
                break;
            case 'drop':
                while (this.valid(0, 1)) {
                    this.currentY++;
                }
                this.tick();
                break;
        }
    }

    // draw a single square at (x, y)
    drawBlock(x, y) {
        this.ctx.fillRect(this.BLOCK_W * x, this.BLOCK_H * y, this.BLOCK_W - 1, this.BLOCK_H - 1);
        this.ctx.strokeRect(this.BLOCK_W * x, this.BLOCK_H * y, this.BLOCK_W - 1, this.BLOCK_H - 1);
    }

    // draws the board and the moving shape
    render() {
        this.ctx.clearRect(0, 0, this.W, this.H);
        this.ctx.strokeStyle = 'black';
        for (let x = 0; x < this.COLS; ++x) {
            for (let y = 0; y < this.ROWS; ++y) {
                if (this.board[y][x]) {
                    this.ctx.fillStyle = this.colors[this.board[y][x] - 1];
                    this.drawBlock(x, y);
                }
            }
        }

        this.ctx.fillStyle = 'red';
        this.ctx.strokeStyle = 'black';
        for (let y = 0; y < 4; ++y) {
            for (let x = 0; x < 4; ++x) {
                if (this.current[y][x]) {
                    this.ctx.fillStyle = this.colors[this.current[y][x] - 1];
                    this.drawBlock(this.currentX + x, this.currentY + y);
                }
            }
        }
    }

    // 尝试根据参数自己走向想到的位置
    forwardToPos(res) {
        let x = res[0];
        let y = res[1];
        let rotateId = res[2];
        let tmpRotate = this.current;
        for (let i = 0; i < rotateId; i++) {
            tmpRotate = Tetris.rotate(tmpRotate)
        }
        if (this.valid(x, 19-y, tmpRotate)) {
            this.currentX = x;
            this.currentY = 19 - y;
            for (let i = 0; i < rotateId; i++) {
                this.current = Tetris.rotate(this.current);
            }
            this.render();
        } else {
            alert("位置错误！你想到的位置坐标为x=" + x + ";y=" + y);
        }

    }

    // 自己走函数位置合法性判定
    forwardValid(x, y, rotateId) {
        switch (this.blockid) {
            case 0:
                return this.checkL(x, y, rotateId);
            case 1:
                return this.checkJ(x, y, rotateId);
            case 2:
                return this.checkS(x, y, rotateId);
            case 3:
                return this.checkZ(x, y, rotateId);
            case 4:
                return this.checkT(x, y, rotateId);
            case 5:
                return this.checkI(x, y, rotateId);
            case 6:
                return this.checkO(x, y, rotateId);
            default:
                return false;
        }

    }

    checkL(x, y, rotateId) {
        if(y < 0 || y >= this.COLS || x < 0 || x >= this.ROWS)
            return false;
        else if (rotateId === 0) {
            if( typeof this.board[x][-y + 20 - 1] === "undefined"
                || typeof this.board[x][-y + 20] === "undefined"
                || typeof this.board[x + 1][-y + 20] === "undefined"
                || typeof this.board[x + 2][-y + 20] === "undefined"
            )
                return false;
            else
                return !(this.board[x][-y + 20 - 1] > 0 || this.board[x][-y + 20] > 0 || this.board[x + 1][-y + 20] > 0 || this.board[x + 2][-y + 20] > 0);
        } else if (rotateId === 1) {
            if(typeof this.board[x][-y + 20] === "undefined"
                || typeof this.board[x + 1][-y + 20] === "undefined"
                || typeof this.board[x + 1][-y + 20 - 1] === "undefined"
                || typeof this.board[x + 1][-y + 20 - 2] === "undefined"
            )
                return false;
            else
                return !(this.board[x][-y + 20] > 0 || this.board[x + 1][-y + 20] > 0 || this.board[x + 1][-y + 20 - 1] > 0 || this.board[x + 1][-y + 20 - 2] > 0);
        } else if (rotateId === 2) {
            if(typeof this.board[x][-y + 20] === "undefined"
                || typeof this.board[x - 2][-y + 20 + 1] === "undefined"
                || typeof this.board[x - 1][-y + 20 + 1] === "undefined"
                || typeof this.board[x][-y + 20 + 1] === "undefined"
            )
                return false;
            else
                return !(this.board[x][-y + 20] > 0 || this.board[x - 2][-y + 20 + 1] > 0 || this.board[x - 1][-y + 20 + 1] > 0 || this.board[x][-y + 20 + 1] > 0);
        } else if (rotateId === 3) {
            if(typeof this.board[x][-y + 20] === "undefined"
                || typeof this.board[x][-y + 20 + 1] === "undefined"
                || typeof this.board[x][-y + 20 + 2] === "undefined"
                || typeof this.board[x + 1][-y + 20 + 2] === "undefined"
            )
                return false;
            else
                return !(this.board[x][-y + 20] > 0 || this.board[x][-y + 20 + 1] > 0 || this.board[x][-y + 20 + 2] > 0 || this.board[x + 1][-y + 20 + 2] > 0);
        } else {
            return false;
        }
    }

    checkJ(x, y, rotateId) {
        if (rotateId === 0) {

            return !(this.board[x][-y + 20 - 1] > 0 || this.board[x][-y + 20] > 0 || this.board[x + 1][-y + 20] > 0 || this.board[x + 2][-y + 20 + 2] > 0);
        } else if (rotateId === 1) {
            return !(this.board[x][-y + 20] > 0 || this.board[x][-y + 20 + 1] > 0 || this.board[x][-y + 20 + 2] > 0 || this.board[x - 1][-y + 20 + 2] > 0);
        } else if (rotateId === 2) {
            return !(this.board[x][-y + 20] > 0 || this.board[x][-y + 20 + 1] > 0 || this.board[x + 1][-y + 20 + 1] > 0 || this.board[x + 2][-y + 20 + 1] > 0);
        } else if (rotateId === 3) {
            return !(this.board[x][-y + 20] > 0 || this.board[x + 1][-y + 20] > 0 || this.board[x][-y + 20 + 1] > 0 || this.board[x][-y + 20 + 2] > 0);
        } else {
            return false;
        }
    }

    checkS(x, y, rotateId) {
        if (rotateId === 0) {
            return !(this.board[x][-y + 20] > 0 || this.board[x + 1][-y + 20] > 0 || this.board[x - 1][-y + 20 + 1] > 0 || this.board[x][-y + 20 + 1] > 0);
        } else if (rotateId === 1) {
            return !(this.board[x][-y + 20] > 0 || this.board[x][-y + 20 + 1] > 0 || this.board[x + 1][-y + 20 + 1] > 0 || this.board[x + 1][-y + 20 + 2] > 0);
        } else if (rotateId === 2) {
            return !(this.board[x][-y + 20] > 0 || this.board[x + 1][-y + 20] > 0 || this.board[x - 1][-y + 20 + 1] > 0 || this.board[x][-y + 20 + 1] > 0);
        } else if (rotateId === 3) {
            return !(this.board[x][-y + 20] > 0 || this.board[x][-y + 20 + 1] > 0 || this.board[x + 1][-y + 20 + 1] > 0 || this.board[x + 1][-y + 20 + 2] > 0);
        } else {
            return false;
        }
    }

    checkZ(x, y, rotateId) {
        if (rotateId === 0) {
            return !(this.board[x][-y + 20] > 0 || this.board[x + 1][-y + 20] > 0 || this.board[x + 1][-y + 20 + 1] > 0 || this.board[x + 2][-y + 20 + 1] > 0);
        } else if (rotateId === 1) {
            return !(this.board[x][-y + 20] > 0 || this.board[x - 1][-y + 20 + 1] > 0 || this.board[x][-y + 20 + 1] > 0 || this.board[x - 1][-y + 20 + 2] > 0);
        } else if (rotateId === 2) {
            return !(this.board[x])
        } else if (rotateId === 3) {
            return !(this.board[x][-y + 20] > 0 || this.board[x - 1][-y + 20 + 1] > 0 || this.board[x][-y + 20 + 1] > 0 || this.board[x - 1][-y + 20 + 2] > 0);
        } else {
            return false;
        }
    }

    checkT(x, y, rotateId) {
        if (rotateId === 0) {
            return !(this.board[x][-y + 20] > 0 || this.board[x - 1][-y + 20 + 1] > 0 || this.board[x][-y + 20 + 1] > 0 || this.board[x + 1][-y + 20 + 1] > 0);
        } else if (rotateId === 1) {
            return !(this.board[x][-y + 20] > 0 || this.board[x][-y + 20 + 1] > 0 || this.board[x + 1][-y + 20 + 1] > 0 || this.board[x][-y + 20 + 2] > 0);
        } else if (rotateId === 2) {
            return !(this.board[x][-y + 20] > 0 || this.board[x + 1][-y + 20] > 0 || this.board[x + 2][-y + 20] > 0 || this.board[x + 1][-y + 20 + 1] > 0);
        } else if (rotateId === 3) {
            return !(this.board[x][-y + 20] > 0 || this.board[x - 1][-y + 20 + 1] > 0 || this.board[x][-y + 20 + 1] > 0 || this.board[x][-y + 20 + 2] > 0);
        } else {
            return false;
        }
    }

    checkI(x, y, rotateId) {
        if (rotateId === 0) {
            return !(this.board[x][-y + 20] > 0 || this.board[x + 1][-y + 20] > 0 || this.board[x + 2][-y + 20] > 0 || this.board[x + 3][-y + 20] > 0);
        } else if (rotateId === 1) {
            return !(this.board[x][-y + 20] > 0 || this.board[x][-y + 20 + 1] > 0 || this.board[x][-y + 20 + 2] > 0 || this.board[x][-y + 20 + 3] > 0);
        } else if (rotateId === 2) {
            return !(this.board[x][-y + 20] > 0 || this.board[x + 1][-y + 20] > 0 || this.board[x + 2][-y + 20] > 0 || this.board[x + 3][-y + 20] > 0);
        } else if (rotateId === 3) {
            return !(this.board[x][-y + 20] > 0 || this.board[x][-y + 20 + 1] > 0 || this.board[x][-y + 20 + 2] > 0 || this.board[x][-y + 20 + 3] > 0);
        } else {
            return false;
        }
    }

    checkO(x, y, rotateId) {
        if (rotateId === 0) {
            return !(this.board[x][-y + 20] > 0 || this.board[x + 1][-y + 20] > 0 || this.board[x][-y + 20 + 1] > 0 || this.board[x + 1][-y + 20 + 1] > 0);
        } else if (rotateId === 1) {
            return !(this.board[x][-y + 20] > 0 || this.board[x + 1][-y + 20] > 0 || this.board[x][-y + 20 + 1] > 0 || this.board[x + 1][-y + 20 + 1] > 0);
        } else if (rotateId === 2) {
            return !(this.board[x][-y + 20] > 0 || this.board[x + 1][-y + 20] > 0 || this.board[x][-y + 20 + 1] > 0 || this.board[x + 1][-y + 20 + 1] > 0);
        } else if (rotateId === 3) {
            return !(this.board[x][-y + 20] > 0 || this.board[x + 1][-y + 20] > 0 || this.board[x][-y + 20 + 1] > 0 || this.board[x + 1][-y + 20 + 1] > 0);
        } else {
            return false;
        }
    }

    //转换函数区域
    transL(x, y, rotateId){
        let res= [];
        if(rotateId === 0){
            res.push(x,22-y,3)
        }else if(rotateId === 1){
            res.push(x,19-y,0);
        }else if(rotateId === 2){
            res.push(x-3,19-y,1);
        }else{
            res.push(x-3,22-y,2);
        }
        return res;
    }

    transJ(x,y,rotateId){
        let res = [];
        if(rotateId === 0){
            res.push(x-3,21-y,1)
        }else if(rotateId === 1){
            res.push(x-1,22-y,2);
        }else if(rotateId === 2){
            res.push(x,20-y,3);
        }else{
            res.push(x-2,19-y,0);
        }
        return res;
    }

    transS(x,y,rotateId){
        let res = [];
        if(rotateId === 0){
            res.push(x-2,20-y,1);
        }else{
            res.push(x-1,19-y,0);
        }
        return res;
    }

    transZ(x,y,rotateId){
        let res = [];
        if(rotateId === 0){
            res.push(x-1,19-y,0)
        }else{
            res.push(x-3,20-y,1);
        }
        return res;
    }

    transT(x,y,rotateId){
        let res = [];
        if(rotateId === 0){
            res.push(x-1,20-y,0)
        }else if(rotateId === 1){
            res.push(x-2,20-y,1);
        }else if(rotateId === 2){
            res.push(x-2,21-y,2);
        }else{
            res.push(x-1,21-y,3);
        }
        return res;
    }

    transI(x,y,rotateId){
        let res = [];
        if(rotateId === 0){
            res.push(x-1,19-y,0);
        }else{
            res.push(x-3,20-y,1);
        }
        return res;
    }

    transO(x,y,rotateId){
        return [x,19-y,0];
    }
}
