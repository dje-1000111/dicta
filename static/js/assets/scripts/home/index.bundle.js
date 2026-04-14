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

/***/ "./assets/scripts/home/get_definition.js":
/*!***********************************************!*\
  !*** ./assets/scripts/home/get_definition.js ***!
  \***********************************************/
/***/ (() => {

eval("let subh = document.getElementById(\"subh\")\r\nif (document.querySelector(\"main\")) {\r\n    var main = document.querySelector(\"main\")\r\n}\r\n\r\ndocument.addEventListener(\"dblclick\", GetSelectedText)\r\n\r\nvar divContainer = document.getElementById(\"dictionary\")\r\nvar divTitle = document.getElementById(\"dictionary-title\")\r\n\r\nfunction GetSelectedText() {\r\n    if (window.getSelection) {\r\n        var range = window.getSelection();\r\n        var text = range.toString()\r\n        var punctuation = ['.', ',', ':', ';', '!', '?', '%', '/', '<', '>', '&', '#', '£', '§', '\"', '{', '}', '(', ')', '@', '[', ']', '⭐']\r\n        for (char of text) {\r\n            if (punctuation.includes(char)) text = text.replace(char, \"\")\r\n        }\r\n        if (text.length > 0) dictmod.show();\r\n    }\r\n\r\n    if (!punctuation.includes(text) && text.length > 0 && text.length < 27) fetch(prde, { //post_request_definition\r\n        method: 'POST',\r\n        headers: {\r\n            'Content-Type': 'application/json',\r\n            \"X-CSRFToken\": csrftoken\r\n        },\r\n        body: JSON.stringify(text)\r\n    })\r\n        .then(async (response) => response.json())\r\n        .then(data => {\r\n            var defs = JSON.parse(data.defs)\r\n            if (document.getElementById(\"dictionary-content\")) document.getElementById(\"dictionary-content\").remove()\r\n            divTitle.innerHTML = \"\"\r\n            let div = document.createElement(\"div\")\r\n            div.id = \"dictionary-content\"\r\n            divTitleContent = document.createTextNode(`${text.charAt(0).toUpperCase() + text.slice(1)}`)\r\n            divTitle.appendChild(divTitleContent)\r\n            if (data.defs.includes(\"no-result\")) {\r\n                var p = document.createElement(\"p\")\r\n                pContent = document.createTextNode(\"No Definition found.\")\r\n                p.appendChild(pContent)\r\n                div.appendChild(p)\r\n            } else {\r\n                for (const [key, value] of Object.entries(defs)) {\r\n                    if (Object.keys(value).length > 0) {\r\n                        var ul = document.createElement(\"ul\")\r\n                        ul.className = \"title\"\r\n                        var ulTitle = document.createTextNode(`${key}`)\r\n                        var li = document.createElement(\"li\")\r\n                        li.appendChild(ulTitle)\r\n                        ul.appendChild(li)\r\n                        div.appendChild(ul)\r\n                        var ul = document.createElement(\"ul\")\r\n                        ul.className = \"def\"\r\n                        for (const [k, v] of Object.entries(value)) {\r\n                            let liContentDef = document.createTextNode(`${v}`)\r\n                            var li = document.createElement(\"li\")\r\n                            if (v == \"Missing definition in Wiktionary.\") {\r\n                                li.className = \"missing\"\r\n                            }\r\n                            li.appendChild(liContentDef);\r\n                            ul.appendChild(li);\r\n                            div.appendChild(ul)\r\n                        }\r\n                    }\r\n                }\r\n            }\r\n            divContainer.appendChild(div)\r\n        })\r\n}\n\n//# sourceURL=webpack://dictatube/./assets/scripts/home/get_definition.js?");

/***/ }),

/***/ "./assets/scripts/home/index.js":
/*!**************************************!*\
  !*** ./assets/scripts/home/index.js ***!
  \**************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _get_definition__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./get_definition */ \"./assets/scripts/home/get_definition.js\");\n/* harmony import */ var _get_definition__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_get_definition__WEBPACK_IMPORTED_MODULE_0__);\n/* harmony import */ var _status_bar__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./status_bar */ \"./assets/scripts/home/status_bar.js\");\n\r\n\n\n//# sourceURL=webpack://dictatube/./assets/scripts/home/index.js?");

/***/ }),

/***/ "./assets/scripts/home/status_bar.js":
/*!*******************************************!*\
  !*** ./assets/scripts/home/status_bar.js ***!
  \*******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   statusBar: () => (/* binding */ statusBar)\n/* harmony export */ });\n/**\r\n * Generate the visual state of an exercise.\r\n * A progress bar for an exercise in progress\r\n * An eye to signify that the exercise has been watched\r\n * An check icon to signify the exercise done \r\n * @constructor\r\n * @param {string} dictationProgress - The percentage calculation.\r\n * @param {Number} dictationId - The ID of the exercise.\r\n * @param {Number} linesLength - The Length of the array \"lines\".\r\n * @param {Boolean} isDone - The status of the exercise.\r\n */\r\nfunction statusBar(dictationProgress, dictationId, linesLength, isDone) {\r\n    var personalProgress = document.getElementById(`your-progress-${dictationId}`)\r\n    var star = document.querySelectorAll(\"#star\")\r\n    // var starsLst = Array.from(star)\r\n    // console.log(\"starsLst\", starsLst.length, starsLst.slice(-1), starsLst)//.nextSibling)[1].nextSibling === null\r\n    if (linesLength === 0) {\r\n        var iEye = document.createElement(\"i\")\r\n        iEye.classList.add(\"fa-solid\")\r\n        iEye.classList.add(\"fa-eye\")\r\n        personalProgress.appendChild(iEye)\r\n    }\r\n    else if (isDone == true) {\r\n        var iSuccess = document.createElement(\"i\")\r\n        iSuccess.classList.add(\"fa-solid\")\r\n        iSuccess.classList.add(\"fa-check\")\r\n        iSuccess.classList.add(\"text-success\")\r\n        personalProgress.appendChild(iSuccess)\r\n    } else {\r\n        var progress = document.createElement(\"div\")\r\n        progress.className = \"progress\"\r\n        progress.setAttribute(\"role\", \"progressbar\");\r\n        progress.setAttribute(\"aria-label\", \"your progress\");\r\n        progress.setAttribute(\"aria-valuenow\", \"0\");\r\n        progress.setAttribute(\"aria-valuemin\", \"0\");\r\n        progress.setAttribute(\"aria-valuemax\", \"100\");\r\n        var progressBar = document.createElement(\"div\")\r\n        progressBar.className = \"progress-bar\"\r\n        progressBar.style.setProperty(\"--dynamic-width\", dictationProgress)\r\n        progressBar.classList.add('progressbar-width');\r\n        let pbContent = document.createTextNode(dictationProgress);\r\n        progress.appendChild(progressBar)\r\n        progressBar.appendChild(pbContent)\r\n        personalProgress.appendChild(progress)\r\n    }\r\n}\r\n\r\n\r\nwindow.statusbar = statusBar;\n\n//# sourceURL=webpack://dictatube/./assets/scripts/home/status_bar.js?");

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
/******/ 	var __webpack_exports__ = __webpack_require__("./assets/scripts/home/index.js");
/******/ 	
/******/ })()
;