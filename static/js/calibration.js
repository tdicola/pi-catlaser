var calibration = function() {
    var calibrateLayer,
        canvas,
        targets,
        bounds,
        targetCal,
        servoCal,
        description = $('#calibrationStep p.description').first(),
        leftButton = $('#calibrationStep button.pull-left').first(),
        rightButton = $('#calibrationStep button.pull-right').first(),
        tempServoCal,
        isCalibrating = false;

    // Load calibration data from the server
    var getCalibration = function() {
        return $.get('/get/calibration')
                    .done(function(cal) {
                        targetCal = cal.target;
                        servoCal = cal.servo;
                    });
    };

            // Save calibration data to the server
    var setCalibration = function() {
        updateTargetCal();
        $.post('/set/calibration', {
            'targetCalibration': JSON.stringify(targetCal),
            'servoCalibration': JSON.stringify(servoCal)
        });
    };

    // Update targetCal data with current target positions
    var updateTargetCal = function() {
        // Update target calibration from current target circle positions
        $.each(targets, function(i, target) {
            targetCal[i].x = target.attr('cx');
            targetCal[i].y = target.attr('cy');
        });
    };

    // Update targets to have current target calibration positions
    var updateTargets = function() {
        $.each(targets, function(i, target) {
            target.attr({cx: targetCal[i].x, cy: targetCal[i].y });
        });      
    };

    // Generate path string for outline of target bounds
    var getBoundsPath = function() {
        return Raphael.fullfill('M{tc1.attrs.cx},{tc1.attrs.cy}L{tc2.attrs.cx},{tc2.attrs.cy}L{tc3.attrs.cx},{tc3.attrs.cy}L{tc4.attrs.cx},{tc4.attrs.cy}Z', {
            tc1: targets[0],
            tc2: targets[1],
            tc3: targets[2],
            tc4: targets[3]
        });
    };

    // Transitions to different calibration states
    var clearClickHandlers = function() {
        leftButton.unbind('click');
        rightButton.unbind('click');
    };

    var startCalibrationState = function() {
        clearClickHandlers();
        description.text('');
        rightButton.hide();
        leftButton.text('Start Calibration');
        leftButton.show();
        leftButton.click(function() {
            targetCalibrationState();
        });
        targets.hide();
        tempServoCal = [];
        tempServoCal.push({x: 0, y: 0});
        tempServoCal.push({x: 0, y: 0});
        tempServoCal.push({x: 0, y: 0});
        tempServoCal.push({x: 0, y: 0});
        isCalibrating = false;
        updateTargets();
        bounds.attr('path', Raphael.parsePathString(getBoundsPath()));
        calibrateLayer.css('cursor', 'crosshair');
    };

    var targetCalibrationState = function() {
        clearClickHandlers();
        description.text('Drag the red circles to form a target area on the screen.  Please make sure the target area is convex--a square of trapezoid is best.');
        rightButton.text('Next');
        leftButton.text('Back');
        rightButton.click(function() {
            servoCorner1State();
        });
        leftButton.click(function() {
            startCalibrationState();
        });
        rightButton.show();
        leftButton.show();
        targets.show();
        isCalibrating = true;
        calibrateLayer.css('cursor', '');
    };

    var servoCorner1State = function() {
        clearClickHandlers();
        description.text('Use the servo controls to move the laser inside the highlighted circle.');
        rightButton.text('Next');
        leftButton.text('Back');
        rightButton.click(function() {
            tempServoCal[0].x = getServoValue('xaxis');
            tempServoCal[0].y = getServoValue('yaxis');
            servoCorner2State();
        });
        leftButton.click(function() {
            targetCalibrationState();
        });
        rightButton.show();
        leftButton.show();
        targets.hide();
        targets[0].show();
    };

    var servoCorner2State = function() {
        clearClickHandlers();
        description.text('Use the servo controls to move the laser inside the highlighted circle.');
        rightButton.text('Next');
        leftButton.text('Back');
        rightButton.click(function() {
            tempServoCal[1].x = getServoValue('xaxis');
            tempServoCal[1].y = getServoValue('yaxis');
            servoCorner3State();
        });
        leftButton.click(function() {
            servoCorner1State();
        });
        rightButton.show();
        leftButton.show();
        targets.hide();
        targets[1].show();
    };

    var servoCorner3State = function() {
        clearClickHandlers();
        description.text('Use the servo controls to move the laser inside the highlighted circle.');
        rightButton.text('Next');
        leftButton.text('Back');
        rightButton.click(function() {
            tempServoCal[2].x = getServoValue('xaxis');
            tempServoCal[2].y = getServoValue('yaxis');
            servoCorner4State();
        });
        leftButton.click(function() {
            servoCorner2State();
        });
        rightButton.show();
        leftButton.show();
        targets.hide();
        targets[2].show();
    };

    var servoCorner4State = function() {
        clearClickHandlers();
        description.text('Use the servo controls to move the laser inside the highlighted circle.');
        rightButton.text('Finish');
        leftButton.text('Back');
        rightButton.click(function() {
            tempServoCal[3].x = getServoValue('xaxis');
            tempServoCal[3].y = getServoValue('yaxis');
            servoCal = tempServoCal;
            setCalibration();
            updateTargetCal();
            startCalibrationState();
        });
        leftButton.click(function() {
            servoCorner3State();
        });
        rightButton.show();
        leftButton.show();
        targets.hide();
        targets[3].show();
    };

    var getServoValue = function(axis) {
        return Number($('#' + axis + ' input').val());
    };

    // Return functions exposed by the module
    return {
        // Setup the calibration data and targets
        setup: function(id, width, height) {
            calibrateLayer = $('#'+id);
            canvas = Raphael(id, width, height);
            return getCalibration().done(function() {
                // If no calibration available pick sensible defaults
                if (targetCal == null) {
                    targetCal = [];
                    targetCal.push({x: Math.round(width*1/4), y: Math.round(height*1/4)});
                    targetCal.push({x: Math.round(width*3/4), y: Math.round(height*1/4)});
                    targetCal.push({x: Math.round(width*2/3), y: Math.round(height*3/4)});
                    targetCal.push({x: Math.round(width*1/3), y: Math.round(height*3/4)});
                }
                if (servoCal == null) {
                    servoCal = [];
                    servoCal.push({x: 150, y: 150});
                    servoCal.push({x: 650, y: 150});
                    servoCal.push({x: 650, y: 650});
                    servoCal.push({x: 150, y: 650});
                }

                // Setup calibration target circles
                targets = canvas.set();
                $.each(targetCal, function(i, target) {
                    targets.push(canvas.circle(target.x, target.y));
                });
                targets.attr({
                    'r':            10,
                    'stroke':       '#ff0000',
                    'stroke-width': 2,
                    'fill':         '#ff0000',
                    'fill-opacity': 0.01
                });
                targets.drag(
                    function(dx, dy) {
                        this.attr({ cx: this.ox + dx, cy: this.oy + dy });
                        bounds.attr('path', Raphael.parsePathString(getBoundsPath()));
                    },
                    function() {
                        this.ox = this.attr('cx');
                        this.oy = this.attr('cy');
                    }
                );

                // Setup the boundary lines
                bounds = canvas.path(getBoundsPath());
                bounds.attr({
                    'stroke':           '#ff0000',
                    'stroke-width':     3,
                    'stroke-opacity':   0.4
                });
                bounds.toBack();

                // Start in initial state
                startCalibrationState();
            });
        },

        isCalibrating: function() {
            return isCalibrating;
        }
    };
}();
