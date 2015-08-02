(function () {

  this.Modal = function (options) {
    // Initialized to all of the defaults for this thing!
    var settings = {
      animationClass: "fadein",
      hasCloseButton: true,
      content: "",
      target: null,
      maxWidth: 800,
      minWidth: 200,
      hasOverlay: true,
      isFixed: true
    };

    if (options && typeof options === "object") {
      for (key in settings) {
        if (options.hasOwnProperty(key)) {
          settings[key] = options[key]
        }
      }
    }
  }

  Modal.prototype.open = function () {

  }
}())
