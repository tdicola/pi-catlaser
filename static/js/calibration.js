var calibration = function() {
    var canvas,
        targets,
        bounds,
        targetCal,
        servoCal;

    // Load calibration data from the server
    var getCalibration = function() {
        return $.get('/get/calibration')
                    .done(function(cal) {
                        targetCal = cal.target;
                        servoCal = cal.servo;
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

    // Generate path string for outline of target bounds
    var getBoundsPath = function() {
        return Raphael.fullfill('M{tc1.x},{tc1.y}L{tc2.x},{tc2.y}L{tc3.x},{tc3.y}L{tc4.x},{tc4.y}Z', {
            tc1: targetCal[0],
            tc2: targetCal[1],
            tc3: targetCal[2],
            tc4: targetCal[3]
        });
    };

    // Return functions exposed by the module
    return {
        // Setup the calibration data and targets
        setup: function(id, width, height) {
            canvas = Raphael(id, width, height);
            return getCalibration().done(function() {
                // If no calibration available pick sensible defaults
                if (targetCal === null) {
                    targetCal = []
                    targetCal.push({x: Math.round(width*1/4), y: Math.round(height*1/4)});
                    targetCal.push({x: Math.round(width*3/4), y: Math.round(height*1/4)});
                    targetCal.push({x: Math.round(width*2/3), y: Math.round(height*3/4)});
                    targetCal.push({x: Math.round(width*1/3), y: Math.round(height*3/4)});
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
                        updateTargetCal();
                        bounds.attr('path', Raphael.parsePathString(getBoundsPath()));
                    },
                    function() {
                        this.ox = this.attr('cx');
                        this.oy = this.attr('cy');
                    }
                );
                targets.hide();

                // Setup the boundary lines
                bounds = canvas.path(getBoundsPath());
                bounds.attr({
                    'stroke':           '#ff0000',
                    'stroke-width':     3,
                    'stroke-opacity':   0.4
                });
                bounds.toBack();
            });
        },

        // Save calibration data to the server
        save: function() {
            updateTargetCal();
            $.post('/set/calibration', { 
                'targetCalibration': JSON.stringify(targetCal), 
                'servoCalibration': JSON.stringify(servoCal)
            }).done(function() { console.log('good'); });
        },

        getTargetCalibration: function() {
            updateTargetCal();
            return targetCal;
        },

        getServoCalibration: function() {
            return servoCal;
        }
    };
}();