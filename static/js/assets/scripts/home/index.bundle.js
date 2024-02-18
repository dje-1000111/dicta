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

eval("let subh = document.getElementById(\"subh\")\r\nif (document.querySelector(\"main\")) {\r\n    var main = document.querySelector(\"main\")\r\n}\r\n\r\ndocument.addEventListener(\"dblclick\", GetSelectedText)\r\n\r\nvar divContainer = document.getElementById(\"dictionary\")\r\nvar divTitle = document.getElementById(\"dictionary-title\")\r\n\r\nfunction GetSelectedText() {\r\n    if (window.getSelection) {\r\n        var range = window.getSelection();\r\n        var text = range.toString()\r\n        var punctuation = ['.', ',', ':', ';', '!', '?', '%', '/', '<', '>', '&', '#', '\"', '{', '}', '(', ')', '@', '[', ']', ' ', '⭐']\r\n        for (char of text) {\r\n            if (punctuation.includes(char)) text = text.replace(char, \"\")\r\n        }\r\n        if (text.length > 0) dictmod.show();\r\n    }\r\n\r\n    if (!punctuation.includes(text) && text.length > 0 && text.length < 27) fetch(prde, { //post_request_definition\r\n        method: 'POST',\r\n        headers: {\r\n            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',\r\n            \"X-CSRFToken\": csrftoken\r\n        },\r\n        body: JSON.stringify(text)\r\n    }).then(async (response) => {\r\n        if (!response.ok) {\r\n            const text = await response.text()\r\n            throw new Error(text)\r\n        } else {\r\n            var defs = JSON.parse(response.headers.get('definition'))\r\n            if (document.getElementById(\"dictionary-content\")) document.getElementById(\"dictionary-content\").remove()\r\n            divTitle.innerHTML = \"\"\r\n\r\n            let div = document.createElement(\"div\")\r\n            div.id = \"dictionary-content\"\r\n            divTitleContent = document.createTextNode(`${text.charAt(0).toUpperCase() + text.slice(1)}`)\r\n            divTitle.appendChild(divTitleContent)\r\n\r\n            if (Object.keys(defs).includes(\"no-result\")) {\r\n                var p = document.createElement(\"p\")\r\n                pContent = document.createTextNode(\"No Definition found.\")\r\n                div.appendChild(pContent)\r\n            } else {\r\n                for (const [key, value] of Object.entries(defs)) {\r\n                    if (Object.keys(value).length > 0) {\r\n                        var ul = document.createElement(\"ul\")\r\n                        ul.className = \"title\"\r\n                        var ulTitle = document.createTextNode(`${key}`)\r\n                        var li = document.createElement(\"li\")\r\n                        li.appendChild(ulTitle)\r\n                        ul.appendChild(li)\r\n                        div.appendChild(ul)\r\n                        var ul = document.createElement(\"ul\")\r\n                        ul.className = \"def\"\r\n                        for (const [k, v] of Object.entries(value)) {\r\n                            let liContentDef = document.createTextNode(`${v}`)\r\n                            var li = document.createElement(\"li\")\r\n                            li.appendChild(liContentDef);\r\n                            ul.appendChild(li);\r\n                            div.appendChild(ul)\r\n                        }\r\n                    }\r\n                }\r\n            }\r\n            divContainer.appendChild(div)\r\n        }\r\n    })\r\n}\r\n\n\n//# sourceURL=webpack://dictatube/./assets/scripts/home/get_definition.js?");

/***/ }),

/***/ "./assets/scripts/home/index.js":
/*!**************************************!*\
  !*** ./assets/scripts/home/index.js ***!
  \**************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _get_definition__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./get_definition */ \"./assets/scripts/home/get_definition.js\");\n/* harmony import */ var _get_definition__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_get_definition__WEBPACK_IMPORTED_MODULE_0__);\n\r\n// import './toggle_mode'\n\n//# sourceURL=webpack://dictatube/./assets/scripts/home/index.js?");

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