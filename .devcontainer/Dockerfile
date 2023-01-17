ARG ZEPHYR_TAG=latest
FROM zephyrprojectrtos/ci:${ZEPHYR_TAG}

# Set default to bash instead sh
ENV SHELL /bin/bash

RUN add-apt-repository ppa:tiac-systems/doxygen

# Install packages
RUN apt-get -y update && \
	apt-get -y upgrade && \
	apt-get install --no-install-recommends -y \
	doxygen \
	graphviz \
	mscgen \
	latexmk \
	librsvg2-bin \
	texlive-latex-base \
	texlive-latex-extra \
	texlive-fonts-recommended \
	usbutils \
	vim

# Clean up stale packages
RUN apt-get clean -y && \
	apt-get autoremove --purge -y && \
	rm -rf /var/lib/apt/lists/*

# Add bash completion script
ADD ./bash_completion /home/user/.bash_completion
RUN mkdir -p /home/user/.bash_completion.d

# Switch to 'user' context
USER user

RUN mkdir -p /home/user/.vscode-server/extensions

# Set working directory
WORKDIR /workdir
VOLUME ["/workdir"]

# Adjust 'user' home directory permissions
USER root
RUN chown -R user:user /home/user

# Make 'user' default on launch
USER user

# Launch bash shell by default
CMD ["/bin/bash"]