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

# Use newer cmake for debugging option
RUN wget -O - https://apt.kitware.com/keys/kitware-archive-latest.asc 2>/dev/null | gpg --dearmor - | tee /usr/share/keyrings/kitware-archive-keyring.gpg >/dev/null && \
	echo 'deb [signed-by=/usr/share/keyrings/kitware-archive-keyring.gpg] https://apt.kitware.com/ubuntu/ jammy main' | sudo tee /etc/apt/sources.list.d/kitware.list >/dev/null && \
	apt-get update && apt install --no-install-recommends -y cmake

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