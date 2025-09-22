FROM kartoza/geoserver:2.22.0

# Copy custom configuration
COPY ./workspaces /opt/geoserver/data_dir/workspaces
COPY ./styles /opt/geoserver/data_dir/styles
COPY ./gwc /opt/geoserver/data_dir/gwc

# Set permissions
USER root
RUN chown -R geoserver:geoserver /opt/geoserver/data_dir
USER geoserver

# Expose port
EXPOSE 8080

# Start GeoServer
CMD ["/opt/geoserver/bin/startup.sh"]
