function MyQueue() {
        
    //初始化队列（使用数组实现）
    var items = [];

    //向队列（尾部）中插入元素
    this.enqueue = function(element) {
        items.push(element);
    }

    //从队列（头部）中弹出一个元素，并返回该元素
    this.dequeue = function() {
        return items.shift();
    }

    //查看队列最前面的元素（数组中索引为0的元素）
    this.front = function() {
        return items[0];
    }

    //查看队列是否为空，如果为空，返回true；否则返回false
    this.isEmpty = function() {
        return items.length == 0;
    }

    //查看队列的长度
    this.size = function() {
        return items.length;
    }

    //查看队列
    this.print = function() {
        //以字符串形势返回
        return items.toString();
    }

    //返回所有元素（数组）
    this.iter = function() {
        //以字符串形势返回
        return items;
    }
}