from flask import Flask, render_template_string, request, jsonify
import requests
import json
import os
from datetime import datetime

app = Flask(__name__)

API_URL = "https://mock-youtube-api-f3d0c17f0e38.herokuapp.com/api/videos"
PLAYLISTS_FILE = 'playlists.json'

def load_playlists():
    if os.path.exists(PLAYLISTS_FILE):
        with open(PLAYLISTS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_playlists(playlists):
    with open(PLAYLISTS_FILE, 'w') as f:
        json.dump(playlists, f)

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/videos')
def get_videos():
    page = request.args.get('page', 1, type=int)
    query = request.args.get('q', '').lower()
    response = requests.get(f"{API_URL}?page={page}")
    data = response.json()
    
    if query:
        data['videos'] = [video for video in data['videos'] if query in video['title'].lower() or query in video['description'].lower()]
        data['meta']['total'] = len(data['videos'])
    
    return jsonify(data)

@app.route('/playlists', methods=['GET', 'POST'])
def manage_playlists():
    playlists = load_playlists()
    if request.method == 'POST':
        data = request.json
        name = data.get('name')
        videos = data.get('videos', [])
        formatted_videos = []
        for video in videos:
            formatted_video = {
                "comments": 0,  # You might want to fetch this from the API
                "created_at": datetime.now().isoformat(),
                "description": video.get('description', ''),
                "id": video['id'],
                "likes": 0,  # You might want to fetch this from the API
                "thumbnail_url": video.get('thumbnail_url', ''),
                "title": video['title'],
                "updated_at": datetime.now().isoformat(),
                "video_id": video['id'],
                "views": video.get('views', 0)
            }
            formatted_videos.append(formatted_video)
        playlists[name] = formatted_videos
        save_playlists(playlists)
        return jsonify({"message": f"Playlist '{name}' updated successfully"})
    return jsonify(playlists)

@app.route('/playlists/<name>', methods=['GET', 'DELETE'])
def playlist_operations(name):
    playlists = load_playlists()
    if request.method == 'GET':
        if name in playlists:
            return jsonify(playlists[name])
        return jsonify({"error": "Playlist not found"}), 404
    elif request.method == 'DELETE':
        if name in playlists:
            del playlists[name]
            save_playlists(playlists)
            return jsonify({"message": f"Playlist '{name}' deleted successfully"})
        return jsonify({"error": "Playlist not found"}), 404

@app.route('/playlists/<name>/videos/<video_id>', methods=['DELETE'])
def remove_video_from_playlist(name, video_id):
    playlists = load_playlists()
    if name in playlists:
        playlists[name] = [video for video in playlists[name] if video['video_id'] != video_id]
        save_playlists(playlists)
        return jsonify({"message": f"Video removed from playlist '{name}'"})
    return jsonify({"error": "Playlist not found"}), 404

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Video Platform</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100">
    <div class="flex flex-col h-full">
        <header class="bg-white p-4 md:p-6 shadow">
            <div class="container mx-auto flex items-center justify-between">
                <a class="text-2xl font-bold" href="#">Video Platform</a>
                <div class="flex items-center gap-4">
                    <div class="relative w-full max-w-md">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">
                            <circle cx="11" cy="11" r="8"></circle>
                            <path d="m21 21-4.3-4.3"></path>
                        </svg>
                        <input id="searchInput" class="flex h-10 border border-gray-300 bg-white px-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent pl-10 pr-4 py-2 rounded-md w-full" type="text" placeholder="Search videos..." />
                    </div>
                    <button id="createPlaylistBtn" class="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600">Create Playlist</button>
                    <button id="viewPlaylistsBtn" class="bg-green-500 text-white px-4 py-2 rounded-md hover:bg-green-600">View Playlists</button>
                </div>
            </div>
        </header>
        <main class="flex-1 container mx-auto py-8 md:py-12">
            <div id="videos" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 md:gap-8">
                <!-- Video cards will be dynamically inserted here -->
            </div>
            <div class="flex justify-center mt-8 md:mt-12">
                <nav id="pagination" class="flex justify-center space-x-2">
                    <!-- Pagination buttons will be dynamically inserted here -->
                </nav>
            </div>
        </main>
    </div>

    <div id="playlistModal" class="fixed inset-0 bg-black bg-opacity-50 hidden items-center justify-center">
        <div class="bg-white p-6 rounded-lg max-w-lg w-full">
            <h2 class="text-xl font-bold mb-4">Create Playlist</h2>
            <input id="playlistName" type="text" placeholder="Playlist Name" class="w-full p-2 border rounded mb-4">
            <div id="selectedVideos" class="mb-4 max-h-60 overflow-y-auto">
                <!-- Selected videos will be displayed here -->
            </div>
            <div class="flex justify-end">
                <button id="cancelPlaylist" class="bg-gray-300 text-black px-4 py-2 rounded-md mr-2">Cancel</button>
                <button id="savePlaylist" class="bg-blue-500 text-white px-4 py-2 rounded-md">Save Playlist</button>
            </div>
        </div>
    </div>

    <div id="playlistsModal" class="fixed inset-0 bg-black bg-opacity-50 hidden items-center justify-center">
        <div class="bg-white p-6 rounded-lg max-w-lg w-full">
            <h2 class="text-xl font-bold mb-4">Your Playlists</h2>
            <div id="playlistsList" class="mb-4 max-h-60 overflow-y-auto">
                <!-- Playlists will be displayed here -->
            </div>
            <div class="flex justify-end">
                <button id="closePlaylistsModal" class="bg-gray-300 text-black px-4 py-2 rounded-md">Close</button>
            </div>
        </div>
    </div>

    <script>
    let currentPage = 1;
    let selectedVideos = [];

    function fetchVideos(page = 1) {
        const searchTerm = document.getElementById('searchInput').value;
        fetch(`/videos?page=${page}&q=${searchTerm}`)
            .then(response => response.json())
            .then(data => {
                displayVideos(data.videos);
                updatePagination(data.meta.total, data.meta.page);
            });
    }

    function displayVideos(videos) {
        const videosContainer = document.getElementById('videos');
        videosContainer.innerHTML = '';
        videos.forEach(video => {
            const videoCard = createVideoCard(video);
            videosContainer.appendChild(videoCard);
        });
    }

    function createVideoCard(video) {
        const videoCard = document.createElement('div');
        videoCard.className = 'bg-white rounded-lg overflow-hidden shadow-lg group';
        videoCard.innerHTML = `
            <img src="${video.thumbnail_url}" alt="${video.title}" class="w-full h-48 object-cover">
            <div class="p-4">
                <h3 class="text-lg font-medium line-clamp-2">${video.title}</h3>
                <p class="text-sm text-gray-500 line-clamp-2">${video.description}</p>
                <div class="flex items-center justify-between mt-2">
                    <div class="text-sm text-gray-500">${video.views} views</div>
                    <button class="selectVideo bg-blue-500 text-white px-2 py-1 rounded text-sm" data-id="${video.id}">Select</button>
                </div>
            </div>
        `;
        return videoCard;
    }

    function updatePagination(total, current) {
        const paginationContainer = document.getElementById('pagination');
        paginationContainer.innerHTML = '';
        const totalPages = Math.ceil(total / 20);  // Assuming 20 videos per page

        for (let i = 1; i <= totalPages; i++) {
            const button = document.createElement('button');
            button.textContent = i;
            button.className = `px-3 py-1 rounded ${i === current ? 'bg-blue-500 text-white' : 'bg-white text-blue-500'}`;
            button.onclick = () => fetchVideos(i);
            paginationContainer.appendChild(button);
        }
    }

    document.getElementById('videos').addEventListener('click', function(e) {
        if (e.target.classList.contains('selectVideo')) {
            const videoId = e.target.dataset.id;
            const videoCard = e.target.closest('.bg-white');
            const video = {
                id: videoId,
                title: videoCard.querySelector('h3').textContent,
                description: videoCard.querySelector('p').textContent,
                thumbnail_url: videoCard.querySelector('img').src,
                views: parseInt(videoCard.querySelector('.text-gray-500').textContent),
            };
            
            const index = selectedVideos.findIndex(v => v.id === videoId);
            if (index === -1) {
                selectedVideos.push(video);
                e.target.textContent = 'Deselect';
                e.target.classList.remove('bg-blue-500');
                e.target.classList.add('bg-red-500');
            } else {
                selectedVideos.splice(index, 1);
                e.target.textContent = 'Select';
                e.target.classList.remove('bg-red-500');
                e.target.classList.add('bg-blue-500');
            }
        }
    });

    document.getElementById('createPlaylistBtn').addEventListener('click', function() {
        document.getElementById('playlistModal').classList.remove('hidden');
        document.getElementById('playlistModal').classList.add('flex');
        updateSelectedVideos();
    });

    document.getElementById('cancelPlaylist').addEventListener('click', function() {
        document.getElementById('playlistModal').classList.add('hidden');
        document.getElementById('playlistModal').classList.remove('flex');
    });

    document.getElementById('savePlaylist').addEventListener('click', function() {
        const playlistName = document.getElementById('playlistName').value;
        if (playlistName && selectedVideos.length > 0) {
            fetch('/playlists', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name: playlistName, videos: selectedVideos }),
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                document.getElementById('playlistModal').classList.add('hidden');
                document.getElementById('playlistModal').classList.remove('flex');
                selectedVideos = [];
                document.querySelectorAll('.selectVideo').forEach(btn => {
                    btn.textContent = 'Select';
                    btn.classList.remove('bg-red-500');
                    btn.classList.add('bg-blue-500');
                });
            });
        } else {
            alert('Please enter a playlist name and select at least one video.');
        }
    });

    function updateSelectedVideos() {
        const container = document.getElementById('selectedVideos');
        container.innerHTML = '';
        selectedVideos.forEach(video => {
            const div = document.createElement('div');
            div.textContent = video.title;
            container.appendChild(div);
        });
    }

    document.getElementById('searchInput').addEventListener('input', function(e) {
        fetchVideos(1);
    });

    document.getElementById('viewPlaylistsBtn').addEventListener('click', function() {
        fetch('/playlists')
            .then(response => response.json())
            .then(playlists => {
                const playlistsList = document.getElementById('playlistsList');
                playlistsList.innerHTML = '';
                for (const [name, videos] of Object.entries(playlists)) {
                    const playlistDiv = document.createElement('div');
                    playlistDiv.className = 'mb-2';
                    playlistDiv.innerHTML = `
                        <h3 class="font-bold">${name}</h3>
                        <p>${videos.length} videos</p>
                        <button class="viewPlaylist bg-blue-500 text-white px-2 py-1 rounded text-sm mr-2" data-name="${name}">View</button>
                        <button class="deletePlaylist bg-red-500 text-white px-2 py-1 rounded text-sm" data-name="${name}">Delete</button>
                    `;
                    playlistsList.appendChild(playlistDiv);
                }
                document.getElementById('playlistsModal').classList.remove('hidden');
                document.getElementById('playlistsModal').classList.add('flex');
            });
    });

    document.getElementById('closePlaylistsModal').addEventListener('click', function() {
        document.getElementById('playlistsModal').classList.add('hidden');
        document.getElementById('playlistsModal').classList.remove('flex');
    });

    document.getElementById('playlistsList').addEventListener('click', function(e) {
        if (e.target.classList.contains('viewPlaylist')) {
            const playlistName = e.target.dataset.name;
            fetch(`/playlists/${playlistName}`)
                .then(response => response.json())
                .then(videos => {
                    displayVideos(videos);
                    document.getElementById('playlistsModal').classList.add('hidden');
                    document.getElementById('playlistsModal').classList.remove('flex');
                });
        } else if (e.target.classList.contains('deletePlaylist')) {
            const playlistName = e.target.dataset.name;
            if (confirm(`Are you sure you want to delete the playlist "${playlistName}"?`)) {
                fetch(`/playlists/${playlistName}`, { method: 'DELETE' })
                    .then(response => response.json())
                    .then(data => {
                        alert(data.message);
                        e.target.closest('div').remove();
                    });
            }
        }
    });

    // Initial load
    fetchVideos();
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(debug=True)