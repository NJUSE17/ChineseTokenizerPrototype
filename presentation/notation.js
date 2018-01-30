var emptyJson = {
    protagonist: {
        contains: false,
        names: []
    },
    location: {
        contains: false,
        names: []
    },
    regulation: {
        contains: false,
        names: []
    }
};

function copyJson(old) {
    return JSON.parse(JSON.stringify(old));
}

var controller = new Vue({
    el: "#controller",
    data: {
        action: "获取",
        // charsIndices: [],
        // protagonistFlags: [],
        // locationFlags: [],
        // regulationFlags: [],
        // peekFlags: [],
        length: 0,

        charInfos: [],

        start: null,
        end: null,

        notation: {
            x: 0,
            y: 0,
            visible: false
        },

        json: emptyJson,
        _id: null,
        text: ""
    },
    methods: {
        getRawSentence: function () {
            var self = this;
            // self.action = "正在获取";
            $.ajax({
                url: "/notation/get-sentence",
                dataType: "json",
                type: "get",
                success: function (res) {
                    // self.action = "提交";
                    self.charInfos = [];
                    self.start = null;
                    self.end = null;
                    console.log(res);
                    self._id = res._id;
                    self.text = res.text;
                    self.json = {
                        _id: res._id,
                        text: res.text,
                        protagonist: {
                            contains: false,
                            names: []
                        },
                        regulation: {
                            contains: false,
                            names: []
                        },
                        location: {
                            contains: false,
                            names: []
                        }
                    };
                    var chars = res.text.split("");
                    chars.forEach(function (char, index) {
                        self.charInfos.push({
                            char: char,
                            index: index,
                            isProtagonist: false,
                            isLocation: false,
                            isRegulation: false,
                            isPeeked: false
                        });
                    });
                    self.length = self.charInfos.length;
                }
            });
        },

        peek: function (index) {
            // console.log(index);
            if (this.start !== null && this.end !== null) {
                return
            }
            for (var i = 0; i < this.length; i++) {
                this.charInfos[i].isPeeked = this.start !== null && this.end === null && i >= this.start && i <= index;
            }
        },

        select: function (index) {
            if (this.start === null && this.end === null) {
                // 开始选择
                this.start = index;
            } else if (this.start !== null && this.end === null && index >= this.start) {
                // 选择完成
                this.end = index;
                this.notation.visible = true;
                var e = event || window.event;
                // console.log(e);
                this.notation.x = e.clientX;
                this.notation.y = e.clientY;
            }
        },

        // getState: function (stateName, index) {
        //
        //     switch (stateName){
        //         case "peek": return this.peekFlags[index];
        //
        //     }
        // },
        submit: function () {
            // this.action = "提交中";
            var self = this;
            $.ajax({
                url: "/notation/submit-notation",
                contentType: "application/json",
                dataType: "json",
                data: JSON.stringify(self.json),
                type: "POST",
                success: function (res) {
                    self.getRawSentence()

                },
                error: function (err) {
                    console.log(err);

                }
            })
        },


        setState: function (stateName) {
            var self = this;
            var setRange = function (from, to, field) {
                for (var i = from; i <= to; i++) {
                    var info = self.charInfos[i];
                    info.isProtagonist = false;
                    info.isLocation = false;
                    info.isRegulation = false;
                    info.isPeeked = false;
                    if (field) {
                        info[field] = true;
                    }

                }
            };
            switch (stateName) {
                case "cancel":
                    setRange(this.start, this.end, null);
                    this.getJson();
                    break;
                case "protagonist":
                    setRange(this.start, this.end, "isProtagonist");
                    this.getJson();
                    break;
                case "location":
                    setRange(this.start, this.end, "isLocation");
                    this.getJson();
                    break;
                case "regulation":
                    setRange(this.start, this.end, "isRegulation");
                    this.getJson();
                    break;
                default:
                    console.error("no such field " + stateName);
            }
            this.notation.visible = false;
            this.start = null;
            this.end = null;

        },

        getJson: function () {
            this.json = copyJson(emptyJson);
            this.json["_id"] = this._id;
            this.json["text"] = this.text;
            var protagonistBuffer = {
                text: "",
                start: null,
                end: null
            };
            var locationBuffer = {
                text: "",
                start: null,
                end: null
            };
            var regulationBuffer = {
                text: "",
                start: null,
                end: null
            };
            var emptyBuffer = {
                text: "",
                start: null,
                end: null
            };

            for (var i = 0; i <= this.length; i++) {
                var charInfo = this.charInfos[i] || {isProtagonist: false, isLocation: false, isRegulation: false};
                if (charInfo.isProtagonist) {
                    if (protagonistBuffer.start === null) {
                        protagonistBuffer.start = i;
                    }
                    protagonistBuffer.end = i;
                    protagonistBuffer.text += charInfo.char;
                } else {
                    if (protagonistBuffer.end !== null) {
                        // buff 有效
                        this.json.protagonist.names.push(protagonistBuffer);
                        this.json.protagonist.contains = true;
                        protagonistBuffer = copyJson(emptyBuffer);
                    }
                }

                if (charInfo.isLocation) {
                    if (locationBuffer.start === null) {
                        locationBuffer.start = i;
                    }
                    locationBuffer.end = i;
                    locationBuffer.text += charInfo.char;
                } else {
                    if (locationBuffer.end !== null) {
                        // buff 有效
                        this.json.location.names.push(locationBuffer);
                        this.json.location.contains = true;
                        locationBuffer = copyJson(emptyBuffer);
                    }
                }

                if (charInfo.isRegulation) {
                    if (regulationBuffer.start === null) {
                        regulationBuffer.start = i;
                    }
                    regulationBuffer.end = i;
                    regulationBuffer.text += charInfo.char;
                } else {
                    if (regulationBuffer.end !== null) {
                        // buff 有效
                        this.json.regulation.names.push(regulationBuffer);
                        this.json.regulation.contains = true;
                        regulationBuffer = copyJson(emptyBuffer);
                    }
                }

                // 最后冲一次缓存
                // if (protagonistBuffer.end !== null) {
                //     // buff 有效
                //     this.json.protagonist.names.push(protagonistBuffer);
                //     this.json.protagonist.contains = true;
                //     protagonistBuffer = copyJson(emptyBuffer);
                // }
                // if (regulationBuffer.end !== null) {
                //     // buff 有效
                //     this.json.regulation.names.push(regulationBuffer);
                //     this.json.regulation.contains = true;
                //     regulationBuffer = copyJson(emptyBuffer);
                // }
                // if (locationBuffer.end !== null) {
                //     // buff 有效
                //     this.json.location.names.push(locationBuffer);
                //     this.json.location.contains = true;
                //     locationBuffer = copyJson(emptyBuffer);
                // }

            }
            // alert()
            console.log(JSON.stringify(this.json));
        }
    }
});
