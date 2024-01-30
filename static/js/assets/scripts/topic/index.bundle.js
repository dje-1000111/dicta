/*
 * ATTENTION: The "eval" devtool has been used (maybe by default in mode: "development").
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
/******/ (() => { // webpackBootstrap
/******/ 	var __webpack_modules__ = ({

/***/ "./assets/scripts/topic/blur_btn.js":
/*!******************************************!*\
  !*** ./assets/scripts/topic/blur_btn.js ***!
  \******************************************/
/***/ (() => {

eval("const blurDiv = document.getElementById(\"blur\")\r\nif (document.getElementById(\"blur-btn\")) {\r\n    var blurBtn = document.getElementById(\"blur-btn\")\r\n    var iblur = document.getElementById(\"iblur\")\r\n}\r\n\r\nblurStatus = 0\r\n\r\nif (blurBtn) {\r\n    blurBtn.onclick = function blurVideo() {\r\n        if (blurStatus === 0) {\r\n            iblur.classList.replace('fa-droplet', 'fa-droplet-slash')\r\n            blurDiv.classList.add(\"blur-vid\")\r\n            blurStatus = 1\r\n        } else {\r\n            iblur.classList.replace('fa-droplet-slash', 'fa-droplet')\r\n            blurDiv.classList.remove(\"blur-vid\")\r\n            blurStatus = 0\r\n        }\r\n\r\n    }\r\n}\r\n\n\n//# sourceURL=webpack://dictatube/./assets/scripts/topic/blur_btn.js?");

/***/ }),

/***/ "./assets/scripts/topic/call_copy.js":
/*!*******************************************!*\
  !*** ./assets/scripts/topic/call_copy.js ***!
  \*******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   call_cp: () => (/* binding */ call_cp),\n/* harmony export */   texts: () => (/* binding */ texts)\n/* harmony export */ });\n/* harmony import */ var _copy_segment_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./copy_segment.js */ \"./assets/scripts/topic/copy_segment.js\");\n\r\n\r\nvar copies = []\r\nvar texts = []\r\n\r\nfunction call_cp() {\r\n    copies.push(window[`btn${lineNb}`])\r\n    copies.forEach(cpBtn => {\r\n        cpBtn.addEventListener(\"click\", function (e) {\r\n            ;(0,_copy_segment_js__WEBPACK_IMPORTED_MODULE_0__.copySegment)(texts[copies.indexOf(cpBtn)])\r\n        })\r\n    });\r\n}\r\n\r\n\n\n//# sourceURL=webpack://dictatube/./assets/scripts/topic/call_copy.js?");

/***/ }),

/***/ "./assets/scripts/topic/copy_segment.js":
/*!**********************************************!*\
  !*** ./assets/scripts/topic/copy_segment.js ***!
  \**********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   copySegment: () => (/* binding */ copySegment)\n/* harmony export */ });\nasync function copySegment(text) {\r\n    try {\r\n        await navigator.clipboard.writeText(text);\r\n    } catch (err) {\r\n        return console.warn('Failed to copy: ', err);\r\n    }\r\n}\r\n\r\n\r\n\n\n//# sourceURL=webpack://dictatube/./assets/scripts/topic/copy_segment.js?");

/***/ }),

/***/ "./assets/scripts/topic/get_average_rgb.js":
/*!*************************************************!*\
  !*** ./assets/scripts/topic/get_average_rgb.js ***!
  \*************************************************/
/***/ (() => {

eval("var imgb64 = document.getElementById('imgb64')\r\n\r\nif (document.getElementById('imgb64')) {\r\n    var rgb = getAverageRGB(imgb64);\r\n    document.body.style.backgroundColor = `rgb(${rgb.r}, ${rgb.g}, ${rgb.b})`\r\n\r\n    function getAverageRGB(imgEl) {\r\n        /*\r\n            script found on:\r\n            https://stackoverflow.com/questions/2541481/get-average-color-of-image-via-javascript\r\n        */\r\n\r\n        var blockSize = 5, // only visit every 5 pixels\r\n            defaultRGB = { r: 12.9, g: 58.8, b: 95.3 }, // for non-supporting envs\r\n            canvas = document.createElement('canvas'),\r\n            context = canvas.getContext && canvas.getContext('2d'),\r\n            data, width, height,\r\n            i = -4,\r\n            length,\r\n            rgb = { r: 0, g: 0, b: 0 },\r\n            count = 0;\r\n\r\n        if (!context) {\r\n            return defaultRGB;\r\n        }\r\n\r\n        height = canvas.height = imgEl.naturalHeight || imgEl.offsetHeight || imgEl.height;\r\n        width = canvas.width = imgEl.naturalWidth || imgEl.offsetWidth || imgEl.width;\r\n\r\n        context.drawImage(imgEl, 0, 0);\r\n\r\n        try {\r\n            imageData = context.getImageData(0, 0, width, height);\r\n        } catch (e) {\r\n            console.warn('Image not compatible'); // security error, img on diff domain \r\n            return defaultRGB;\r\n        }\r\n\r\n        length = imageData.data.length;\r\n\r\n        while ((i += blockSize * 4) < length) {\r\n            ++count;\r\n            rgb.r += imageData.data[i];\r\n            rgb.g += imageData.data[i + 1];\r\n            rgb.b += imageData.data[i + 2];\r\n        }\r\n\r\n        // ~~ used to floor values\r\n        rgb.r = ~~(rgb.r / count);\r\n        rgb.g = ~~(rgb.g / count);\r\n        rgb.b = ~~(rgb.b / count);\r\n\r\n        return rgb\r\n    }\r\n}\r\n\n\n//# sourceURL=webpack://dictatube/./assets/scripts/topic/get_average_rgb.js?");

/***/ }),

/***/ "./assets/scripts/topic/get_definition.js":
/*!************************************************!*\
  !*** ./assets/scripts/topic/get_definition.js ***!
  \************************************************/
/***/ (() => {

eval("let subh = document.getElementById(\"subh\")\r\nif (document.querySelector(\"main\")) {\r\n    var main = document.querySelector(\"main\")\r\n}\r\n\r\ndocument.addEventListener(\"dblclick\", GetSelectedText)\r\n\r\nfunction GetSelectedText() {\r\n    if (window.getSelection) {\r\n        var range = window.getSelection();\r\n        var text = range.toString()\r\n    }\r\n\r\n    fetch(prde, { //post_request_definition\r\n        method: 'POST',\r\n        headers: {\r\n            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',\r\n            \"X-CSRFToken\": csrftoken\r\n        },\r\n        body: JSON.stringify(text)\r\n    }).then(async (response) => {\r\n        if (!response.ok) {\r\n            const text = await response.text()\r\n            throw new Error(text)\r\n        } else {\r\n\r\n            if (document.getElementById(\"tt\")) document.getElementById(\"tt\").remove()\r\n\r\n            if (document.getElementById(\"define\")) document.getElementById(\"define\").remove()\r\n            let div = document.createElement(\"div\")\r\n            let divContainer = document.createElement(\"div\")\r\n            divContainer.id = \"define\"\r\n            divContainer.className = \"def-container\"\r\n            let spanCross = document.createElement(\"span\")\r\n            spanCross.className = \"cross\"\r\n            let divTitle = document.createElement(\"div\")\r\n            divTitle.className = \"deft\"\r\n            divTitleContent = document.createTextNode(`${text.charAt(0).toUpperCase() + text.slice(1)}`)\r\n            divTitle.appendChild(divTitleContent)\r\n            divTitle.prepend(spanCross)\r\n            div.className = \"winbox\"\r\n            let ul = document.createElement(\"ul\")\r\n\r\n            var defs = JSON.parse(response.headers.get('definition'))\r\n            for (let i = 0; i < Object.keys(defs).length; i++) {\r\n                var li = document.createElement(\"li\")\r\n                let liContent = document.createTextNode(`${defs[i]}`)\r\n                li.appendChild(liContent)\r\n                ul.appendChild(li)\r\n            }\r\n\r\n            if (Object.keys(defs).length > 0) {\r\n                div.prepend(ul)\r\n                divContainer.prepend(div)\r\n                divContainer.prepend(divTitle)\r\n\r\n                let box = subh ? subh : main\r\n                box.prepend(divContainer)\r\n            }\r\n\r\n            var define = document.getElementById(\"define\")\r\n            spanCross.addEventListener(\"click\", function () {\r\n                define.remove()\r\n                let divtt = document.createElement(\"div\")\r\n                divtt.id = \"tt\"\r\n                divtt.className = \"tooltipz\"\r\n                divttContent = document.createTextNode(\"Get word definition\")\r\n                divtt.appendChild(divttContent)\r\n                let spantt = document.createElement(\"span\")\r\n                spantt.className = \"bg-info p-2 float-end mb-3 tooltiptext\"\r\n                spanttContent = document.createTextNode(\"Double click on a word to get its definition\")\r\n                spantt.appendChild(spanttContent)\r\n                divtt.prepend(spantt)\r\n                main.prepend(divtt)\r\n            })\r\n        }\r\n    })\r\n}\r\n\n\n//# sourceURL=webpack://dictatube/./assets/scripts/topic/get_definition.js?");

/***/ }),

/***/ "./assets/scripts/topic/index.js":
/*!***************************************!*\
  !*** ./assets/scripts/topic/index.js ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _get_definition__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./get_definition */ \"./assets/scripts/topic/get_definition.js\");\n/* harmony import */ var _get_definition__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_get_definition__WEBPACK_IMPORTED_MODULE_0__);\n/* harmony import */ var _blur_btn__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./blur_btn */ \"./assets/scripts/topic/blur_btn.js\");\n/* harmony import */ var _blur_btn__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_blur_btn__WEBPACK_IMPORTED_MODULE_1__);\n/* harmony import */ var _call_copy__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./call_copy */ \"./assets/scripts/topic/call_copy.js\");\n/* harmony import */ var _copy_segment__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./copy_segment */ \"./assets/scripts/topic/copy_segment.js\");\n/* harmony import */ var _get_average_rgb__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./get_average_rgb */ \"./assets/scripts/topic/get_average_rgb.js\");\n/* harmony import */ var _get_average_rgb__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_get_average_rgb__WEBPACK_IMPORTED_MODULE_4__);\n/* harmony import */ var _post_json_data__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./post_json_data */ \"./assets/scripts/topic/post_json_data.js\");\n/* harmony import */ var _post_rating__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./post_rating */ \"./assets/scripts/topic/post_rating.js\");\n/* harmony import */ var _post_rating__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_post_rating__WEBPACK_IMPORTED_MODULE_6__);\n/* harmony import */ var _put_segment_in_page__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./put_segment_in_page */ \"./assets/scripts/topic/put_segment_in_page.js\");\n/* harmony import */ var _playstop_video__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./playstop_video */ \"./assets/scripts/topic/playstop_video.js\");\n/* harmony import */ var _rm_segment__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./rm_segment */ \"./assets/scripts/topic/rm_segment.js\");\n// import './toggle_mode'\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\n\n//# sourceURL=webpack://dictatube/./assets/scripts/topic/index.js?");

/***/ }),

/***/ "./assets/scripts/topic/playstop_video.js":
/*!************************************************!*\
  !*** ./assets/scripts/topic/playstop_video.js ***!
  \************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _post_json_data_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./post_json_data.js */ \"./assets/scripts/topic/post_json_data.js\");\nconst previous = document.getElementById(\"previous\")\r\nconst goNext = document.getElementById(\"go-next\")\r\nconst playstop = document.getElementById(\"playstop\")\r\nconst iplaystop = document.getElementById(\"iplaystop\")\r\nvar reinit = false\r\n\r\n;\r\n\r\nconst lightbulb = '<i class=\"fa-solid fa-lightbulb\" style=\"color: #ffffff;\"></i>'\r\n\r\n_post_json_data_js__WEBPACK_IMPORTED_MODULE_0__.tipDiv.innerHTML = (tip[lineNb] !== undefined) ? `${lightbulb} TIP: ${tip[lineNb]}` : _post_json_data_js__WEBPACK_IMPORTED_MODULE_0__.tipDiv.innerHTML = \"\"\r\n\r\nif (document.getElementById(\"playstop\")) {\r\n    playstop.addEventListener(\"click\", function (event) {\r\n        if (paused) {\r\n            player.seekTo(ts[lineNb], true)\r\n            window.clearTimeout(timeout);\r\n            player.playVideo()\r\n            done = false\r\n            paused = false\r\n        } else {\r\n            player.pauseVideo()\r\n            paused = true\r\n            iplaystop.classList.replace('fa-stop', 'fa-play')\r\n        }\r\n\r\n    })\r\n}\r\n\r\nif (document.getElementById(\"previous\")) {\r\n    previous.addEventListener(\"click\", function (event) {\r\n        if (lineNb >= 1) lineNb -= 1;\r\n        _post_json_data_js__WEBPACK_IMPORTED_MODULE_0__.tipDiv.innerHTML = (tip[lineNb] !== undefined) ? `${lightbulb}  TIP: ${tip[lineNb]}` : _post_json_data_js__WEBPACK_IMPORTED_MODULE_0__.tipDiv.innerHTML = \"\"\r\n        player.seekTo(ts[lineNb], true)\r\n        counter.innerHTML = lineNb\r\n        lines.includes(lineNb) ? create_level_valid() : del_level_valid()\r\n        window.clearTimeout(timeout);\r\n        player.seekTo(ts[lineNb], true)\r\n        player.playVideo()\r\n        done = false\r\n        reveal.innerHTML = `<i class=\"fa-solid fa-${revealAttempts} w-ctrl\"></i>`\r\n        reinit = true\r\n    })\r\n}\r\n\r\nif (document.getElementById(\"go-next\")) {\r\n    goNext.addEventListener(\"click\", function (event) {\r\n        if (lineNb < totl) lineNb += 1\r\n        _post_json_data_js__WEBPACK_IMPORTED_MODULE_0__.tipDiv.innerHTML = (tip[lineNb] !== undefined) ? `${lightbulb}  TIP: ${tip[lineNb]}` : _post_json_data_js__WEBPACK_IMPORTED_MODULE_0__.tipDiv.innerHTML = \"\"\r\n        player.seekTo(ts[lineNb], true)\r\n        counter.innerHTML = lineNb\r\n        lines.includes(lineNb) ? create_level_valid() : del_level_valid()\r\n        window.clearTimeout(timeout);\r\n        player.seekTo(ts[lineNb], true)\r\n        player.playVideo()\r\n        done = false\r\n        reveal.innerHTML = `<i class=\"fa-solid fa-${revealAttempts} w-ctrl\"></i>`\r\n    })\r\n}\r\n\n\n//# sourceURL=webpack://dictatube/./assets/scripts/topic/playstop_video.js?");

/***/ }),

/***/ "./assets/scripts/topic/post_json_data.js":
/*!************************************************!*\
  !*** ./assets/scripts/topic/post_json_data.js ***!
  \************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   tipDiv: () => (/* binding */ tipDiv)\n/* harmony export */ });\n/* harmony import */ var _put_segment_in_page_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./put_segment_in_page.js */ \"./assets/scripts/topic/put_segment_in_page.js\");\nasync function postJsonData(url, data, headers) {\r\n    try {\r\n        const response = await fetch(url, {\r\n            method: \"POST\",\r\n            body: JSON.stringify(data),\r\n            headers: headers\r\n        });\r\n        return await response.json();\r\n\r\n    } catch (err) {\r\n        return console.warn(err);\r\n    }\r\n}\r\n\r\nconst headers = {\r\n    \"Accept\": \"application/json\",\r\n    \"Content-Type\": \"application/json\",\r\n    \"X-CSRFToken\": csrftoken\r\n}\r\n\r\n;\r\n\r\nif (document.getElementById(\"id_textarea\")) {\r\n    var textarea_content = document.getElementById(\"id_textarea\").value;\r\n}\r\nvar counter = document.getElementById(\"counter\");\r\nvar check = document.getElementById(\"check\");\r\nvar reveal = document.getElementById(\"reveal\");\r\nvar result_correction = document.getElementById(\"result_correction\")\r\nvar currentStamp = 0\r\nvar state = false;\r\nvar revealStatus = false\r\nconst tipDiv = document.getElementById(\"tip\")\r\nvar nextBtn\r\nvar jsonresult\r\nvar original\r\nvar revealAttempts\r\n\r\n\r\n\r\nfunction create_next_button() {\r\n    nextBtn = document.createElement(\"button\")\r\n    let nextBtnText = \"Next\"\r\n    nextBtn.className = \"btn btn-success\";\r\n    nextBtn.id = \"next\"\r\n    let btnNextContent = document.createTextNode(nextBtnText);\r\n    nextBtn.appendChild(btnNextContent);\r\n    document.querySelector(\"#complete\").appendChild(nextBtn);\r\n}\r\n\r\nfunction put_text_valid_class() {\r\n    result_correction.innerHTML = original\r\n    result_correction.classList.add(\"text-valid\")\r\n    result_correction.classList.remove(\"text-invalid\")\r\n}\r\n\r\nfunction put_text_invalid_class() {\r\n    result_correction.classList.add(\"text-invalid\")\r\n    result_correction.classList.remove(\"text-valid\")\r\n    result_correction.innerHTML = jsonresult\r\n}\r\n\r\nfunction display_tip() {\r\n    tipDiv.innerHTML = (tip[lineNb] !== undefined) ? `<i class=\"fa-solid fa-lightbulb\"></i> TIP: ${tip[lineNb]}` : tipDiv.innerHTML = \"\"\r\n}\r\n\r\nfunction init_counter_reveal_button() {\r\n    reveal.innerHTML = `<i class=\"fa-solid fa-${revealAttempts} w-ctrl\"></i>`\r\n}\r\n\r\nfunction common_then() {\r\n    if (revealStatus === true) revealStatus = false\r\n\r\n    reveal.innerHTML = `<i class=\"fa-solid fa-${revealAttempts} w-ctrl\"></i>`\r\n    let nxt = document.getElementById(\"next\")\r\n    if (jsonresult && state === true) {\r\n        put_text_valid_class()\r\n        if (!nxt && lineNb < ts.length - 2) {\r\n            create_next_button()\r\n            nextBtn.onclick = function loadNewSegment() {\r\n                if (lineNb < ts.length - 2 && state === true) {\r\n                    lineNb += 1\r\n                    currentStamp = ts[lineNb];\r\n                    player.seekTo(currentStamp, true)\r\n                    player.playVideo()\r\n                    done = false\r\n                    document.getElementById(\"id_textarea\").value = \"\"\r\n                    state = false\r\n                    result_correction.innerHTML = \"\"\r\n                    revealAttempts = 0\r\n                    init_counter_reveal_button()\r\n                    counter.innerHTML = lineNb\r\n                    lines.push(lineNb - 1)\r\n                    display_tip()\r\n                    ;(0,_put_segment_in_page_js__WEBPACK_IMPORTED_MODULE_0__.putStorySegmentInPage)(original)\r\n                    postJsonData(aptc, {\r\n                        \"lineNb\": lineNb,\r\n                        \"new_text\": textarea_content,\r\n                        \"topicname\": topicname,\r\n                        \"reveal_status\": revealStatus,\r\n                        \"new_page\": true,\r\n                        \"dictation_id\": dictation_id,\r\n                    }, headers)\r\n                }\r\n                nextBtn.remove()\r\n            }\r\n        } else if (lineNb == ts.length - 2 && state === true) {\r\n            // There is another point:\r\n            // if someone only anwser the last question, these congrats are displayed.\r\n            // TODO: change the condition in order to display it only if the lenght of\r\n            // lines == total_line\r\n            // For anyone who do the exercise in a different order, it should be a real advantage\r\n            // to know which line aren't anwsered.\r\n            lines.push(lineNb - 1)\r\n            console.log(\"congrats\", lines, totl)\r\n            result_correction.innerHTML = \"This is the end, nice work, congrats! :)\"\r\n            // These congrats aren't a solution at all. It must be a button or a modal.\r\n            // So the loop is looped !!!\r\n\r\n            //////////////////////////////////!\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\r\n            // may be the solution in order to empty the \"counter\" of help is to\r\n            // display a modal to ask if the user really want to leave the exercise.\r\n            // And so , by validating that modal, he reinitiate the counter.\r\n            // In the case he wants to quit before the end.\r\n            // And, the normal way will be to display a button (or a modal) who is \r\n            // the confirmation of the ended excercise. Same result: reinitiate the counter.\r\n            ;(0,_put_segment_in_page_js__WEBPACK_IMPORTED_MODULE_0__.putStorySegmentInPage)(original)\r\n        }\r\n    } else {\r\n        put_text_invalid_class()\r\n    }\r\n}\r\n\r\nif (check || reveal) {\r\n    let btns = [check, reveal]\r\n    btns.forEach(btn => {\r\n        btn.addEventListener('click', function (event) {\r\n            var textarea_content = document.getElementById(\"id_textarea\").value;\r\n            revealStatus = (btn === reveal) ? true : false\r\n            postJsonData(aptc, {\r\n                \"lineNb\": lineNb,\r\n                \"new_text\": textarea_content,\r\n                \"topicname\": topicname,\r\n                \"reveal_status\": revealStatus,\r\n                \"new_page\": false,\r\n                \"dictation_id\": dictation_id,\r\n            }, headers).then(jsonResponse => {\r\n                jsonresult = jsonResponse.result\r\n                state = jsonResponse.state\r\n                original = jsonResponse.original\r\n                revealAttempts = jsonResponse.reveal_attempts\r\n                common_then()\r\n            })\r\n        })\r\n    });\r\n}\r\n\r\ndocument.addEventListener('keydown', (event) => {\r\n\r\n    if (event.ctrlKey) {\r\n\r\n        if (player) player.seekTo(ts[lineNb], true)\r\n        window.clearTimeout(timeout);\r\n        player.seekTo(ts[lineNb], true)\r\n        player.playVideo()\r\n        done = false\r\n    }\r\n    if (event.key === 'Enter') {\r\n        event.preventDefault();\r\n        let txtAreaContent = document.getElementById(\"id_textarea\").value\r\n        postJsonData(aptc, {\r\n            \"lineNb\": lineNb,\r\n            \"new_text\": txtAreaContent,\r\n            \"topicname\": topicname,\r\n            \"reveal_status\": revealStatus,\r\n            \"new_page\": false,\r\n            \"dictation_id\": dictation_id,\r\n        }, headers).then(jsonResponse => {\r\n            jsonresult = jsonResponse.result\r\n            state = jsonResponse.state\r\n            original = jsonResponse.original\r\n            revealAttempts = jsonResponse.reveal_attempts\r\n            common_then()\r\n        })\r\n    }\r\n})\r\n\n\n//# sourceURL=webpack://dictatube/./assets/scripts/topic/post_json_data.js?");

/***/ }),

/***/ "./assets/scripts/topic/post_rating.js":
/*!*********************************************!*\
  !*** ./assets/scripts/topic/post_rating.js ***!
  \*********************************************/
/***/ (() => {

eval("async function postJsonData(url, data, headers) {\r\n    try {\r\n        const response = await fetch(url, {\r\n            method: 'POST',\r\n            body: JSON.stringify(data),\r\n            dataType: 'json',\r\n            headers: headers,\r\n        })\r\n        return await response.json()\r\n    } catch (err) {\r\n        return console.warn(err)\r\n    }\r\n}\r\n\r\nlet radio = document.querySelectorAll('input[type=radio][name=rate]')\r\n\r\nradio.forEach(function (radiosel) {\r\n    radiosel.addEventListener('change', function (e) {\r\n        e.preventDefault()\r\n        if (radiosel.checked == true) {\r\n            postJsonData(\r\n                aprr,\r\n                {\r\n                    star_rating: e.target.value,\r\n                    dictation_id: e.target.id\r\n                },\r\n                {\r\n                    Accept: 'application/json',\r\n                    'Content-Type': 'application/json',\r\n                    'X-CSRFToken': csrftoken,\r\n                },\r\n            )\r\n        }\r\n    })\r\n})\n\n//# sourceURL=webpack://dictatube/./assets/scripts/topic/post_rating.js?");

/***/ }),

/***/ "./assets/scripts/topic/put_segment_in_page.js":
/*!*****************************************************!*\
  !*** ./assets/scripts/topic/put_segment_in_page.js ***!
  \*****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   putStorySegmentInPage: () => (/* binding */ putStorySegmentInPage),\n/* harmony export */   storySegment: () => (/* binding */ storySegment)\n/* harmony export */ });\n/* harmony import */ var _call_copy_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./call_copy.js */ \"./assets/scripts/topic/call_copy.js\");\n\r\n\r\nvar storySegment = document.getElementById(\"story-segment\")\r\n\r\nfunction putStorySegmentInPage(segment) {\r\n    // slice to ignore '\\n' at the end\r\n    segment = segment.slice(0, -1)\r\n    let li = document.createElement(\"li\")\r\n    let i = document.createElement(\"i\")\r\n    i.className = \"fa-solid fa-copy style='color: #a8bb24;'\"\r\n    window[`textline${counter}`] = document.createTextNode(segment);\r\n    li.appendChild(window[`textline${counter}`]);\r\n    storySegment.appendChild(li);\r\n    _call_copy_js__WEBPACK_IMPORTED_MODULE_0__.texts.push(segment)\r\n    window[`btn${lineNb}`] = document.createElement(\"button\")\r\n    window[`btn${lineNb}`].className = \"btn\"\r\n    window[`btn${lineNb}`].id = `copy-${lineNb}` // facultatif\r\n    window[`btn${lineNb}`].appendChild(i);\r\n    li.appendChild(window[`btn${lineNb}`]);\r\n\r\n    (0,_call_copy_js__WEBPACK_IMPORTED_MODULE_0__.call_cp)()\r\n\r\n}\r\n\r\n\r\n\r\n\n\n//# sourceURL=webpack://dictatube/./assets/scripts/topic/put_segment_in_page.js?");

/***/ }),

/***/ "./assets/scripts/topic/rm_segment.js":
/*!********************************************!*\
  !*** ./assets/scripts/topic/rm_segment.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _put_segment_in_page_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./put_segment_in_page.js */ \"./assets/scripts/topic/put_segment_in_page.js\");\n\r\n\r\nif (document.getElementById(\"previous\")) {\r\n    previous.addEventListener(\"click\", function () {\r\n        if (lineNb > 0 && _put_segment_in_page_js__WEBPACK_IMPORTED_MODULE_0__.storySegment.lastElementChild) {\r\n            _put_segment_in_page_js__WEBPACK_IMPORTED_MODULE_0__.storySegment.removeChild(_put_segment_in_page_js__WEBPACK_IMPORTED_MODULE_0__.storySegment.lastElementChild)\r\n        }\r\n    })\r\n}\r\n\n\n//# sourceURL=webpack://dictatube/./assets/scripts/topic/rm_segment.js?");

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			// no module.id needed
/******/ 			// no module.loaded needed
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId](module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/compat get default export */
/******/ 	(() => {
/******/ 		// getDefaultExport function for compatibility with non-harmony modules
/******/ 		__webpack_require__.n = (module) => {
/******/ 			var getter = module && module.__esModule ?
/******/ 				() => (module['default']) :
/******/ 				() => (module);
/******/ 			__webpack_require__.d(getter, { a: getter });
/******/ 			return getter;
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/define property getters */
/******/ 	(() => {
/******/ 		// define getter functions for harmony exports
/******/ 		__webpack_require__.d = (exports, definition) => {
/******/ 			for(var key in definition) {
/******/ 				if(__webpack_require__.o(definition, key) && !__webpack_require__.o(exports, key)) {
/******/ 					Object.defineProperty(exports, key, { enumerable: true, get: definition[key] });
/******/ 				}
/******/ 			}
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/hasOwnProperty shorthand */
/******/ 	(() => {
/******/ 		__webpack_require__.o = (obj, prop) => (Object.prototype.hasOwnProperty.call(obj, prop))
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/make namespace object */
/******/ 	(() => {
/******/ 		// define __esModule on exports
/******/ 		__webpack_require__.r = (exports) => {
/******/ 			if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 				Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 			}
/******/ 			Object.defineProperty(exports, '__esModule', { value: true });
/******/ 		};
/******/ 	})();
/******/ 	
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module can't be inlined because the eval devtool is used.
/******/ 	var __webpack_exports__ = __webpack_require__("./assets/scripts/topic/index.js");
/******/ 	
/******/ })()
;