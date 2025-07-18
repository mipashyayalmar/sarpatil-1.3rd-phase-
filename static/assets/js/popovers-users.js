/*! popovers-users.js */
"use strict";

function getUserPopovers() {
    $("*[data-user-popover]").each(function() {
        var element = $(this);
        var userId = element.attr("data-user-popover");
        var username = element.attr("data-user-username");
        var firstname = element.attr("data-user-firstname");
        var lastname = element.attr("data-user-lastname");
        var location = element.attr("data-user-location");
        var bio = element.attr("data-user-bio");
        var profileUrl = element.attr("data-user-url");
        var profileImage = element.attr("src") || element.attr("data-demo-src");
        var backgroundImage = element.attr("data-user-background") || "/static/images/default-background.jpg"; // Add this line

        // Feather icons
        var messageIcon = feather.icons["message-circle"].toSvg();
        var moreIcon = feather.icons["more-horizontal"].toSvg();
        var locationIcon = feather.icons["map-pin"].toSvg();
        var friendsIcon = feather.icons.users.toSvg();
        var bookmarkIcon = feather.icons.bookmark.toSvg();

        // Check if we have enough data to show popover without API call
        if (username && profileImage) {
            element.webuiPopover({
                trigger: "hover",
                placement: "auto",
                width: 300,
                padding: false,
                offsetLeft: 0,
                offsetTop: 20,
                animation: "pop",
                cache: false,
                content: function() {
                    setTimeout(function() {
                        $(".loader-overlay").removeClass("is-active");
                    }, 1000);
                    
                    return `
                        <div class="profile-popover-block">
                            <div class="loader-overlay is-active">
                                <div class="loader is-loading"></div>
                            </div>

                            <div class="profile-popover-wrapper">
                                <div class="popover-cover">
                                    <!-- Updated to use background image -->
                                    <img src="${backgroundImage}" style="width: 100%; height: 80px; object-fit: cover;">
                                    <div class="popover-avatar">
                                        <img class="avatar" src="${profileImage}">
                                    </div>
                                </div>

                                <div class="popover-meta">
                                    <span class="user-meta">
                                        <span class="username">${firstname || ''} ${lastname || ''}</span>
                                    </span>
                                    <span class="job-title">@${username}</span>
                                    ${bio ? `<div class="user-bio">${bio}</div>` : ''}
                                    ${location ? `
                                    <div class="user-location">
                                        ${locationIcon}
                                        <div class="text">
                                            From <a href="#">${location}</a>
                                        </div>
                                    </div>` : ''}
                                </div>
                            </div>
                            <div class="popover-actions">
                                <a href="#" class="popover-icon" data-action="more">
                                    ${moreIcon}
                                </a>
                                <a href="#" class="popover-icon" data-action="bookmark">
                                    ${bookmarkIcon}
                                </a>
                                <a href="/profile/${username}" class="popover-icon" data-action="message">
                                    ${messageIcon}
                                </a>
                            </div>
                        </div>
                    `;
                }
            });
        } else {
            // Fallback for cases where we don't have all data attributes
            element.webuiPopover({
                trigger: "hover",
                placement: "auto",
                width: 300,
                padding: false,
                offsetLeft: 0,
                offsetTop: 20,
                animation: "pop",
                cache: false,
                content: function() {
                    return `
                        <div class="profile-popover-block">
                            <div class="profile-popover-wrapper">
                                <div class="popover-cover">
                                    <img src="${backgroundImage}" style="width: 100%; height: 80px; object-fit: cover;">
                                    <div class="popover-avatar">
                                        <img class="avatar" src="${profileImage || '/static/images/default-avatar.png'}">
                                    </div>
                                </div>
                                <div class="popover-meta">
                                    <span class="user-meta">
                                        <span class="username">User</span>
                                    </span>
                                    <div class="text-muted">Loading user information...</div>
                                </div>
                            </div>
                        </div>
                    `;
                }
            });
        }
    });
}

$(document).ready(function() {
    // Initialize feather icons
    feather.replace();
    
    // Initialize popovers
    getUserPopovers();

    // Reinitialize popovers after AJAX content loads (if needed)
    $(document).ajaxComplete(function() {
        feather.replace();
        getUserPopovers();
    });
});